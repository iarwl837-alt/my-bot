import concurrent.futures
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ضع توكن البوت الخاص بك هنا الذي استخرجته من BotFather
TOKEN = "8668281614:AAE6hkkrjqB8blJqewbOjrzEEPzztv21Zq8"

TEST_URL = "https://httpbin.org/ip"
TIMEOUT = 5


def check_proxy(proxy):
  proxy_url = proxy if "://" in proxy else f"http://{proxy}"
  proxies = {"http": proxy_url, "https": proxy_url}

  try:
    response = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
    if response.status_code == 200:
      return proxy
  except requests.exceptions.RequestException:
    pass
  return None


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
  document = update.message.document

  # التأكد أن الملف المرسل هو بصيغة نصية txt
  if not document.file_name.endswith(".txt"):
    await update.message.reply_text("الرجاء إرسال ملف بصيغة .txt يحتوي على البروكسيات.")
    return

  await update.message.reply_text(
      "جاري تحميل الملف وفحص البروكسيات، قد يستغرق ذلك بعض الوقت..."
  )

  # تحميل الملف إلى السيرفر مؤقتاً
  file = await context.bot.get_file(document.file_id)
  input_path = "input_proxies.txt"
  output_path = "live_proxies.txt"

  await file.download_to_drive(input_path)

  # قراءة البروكسيات
  with open(input_path, "r", encoding="utf-8") as f:
    proxies_list = [line.strip() for line in f if line.strip()]

  if not proxies_list:
    await update.message.reply_text("الملف فارغ!")
    return

  # فحص البروكسيات باستخدام ThreadPoolExecutor
  live_proxies = []
  with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(check_proxy, proxies_list)
    for r in results:
      if r:
        live_proxies.append(r)

  # حفظ النتائج
  with open(output_path, "w", encoding="utf-8") as f:
    for p in live_proxies:
      f.write(f"{p}\n")

  # إرسال الملف الناتج للمستخدم
  with open(output_path, "rb") as f:
    await update.message.reply_document(
        document=f,
        filename="live_proxies.txt",
        caption=(
            f"انتهى الفحص!\n"
            f"البروكسيات الإجمالية: {len(proxies_list)}\n"
            f"البروكسيات الحية: {len(live_proxies)}"
        ),
    )

  # تنظيف الملفات المؤقتة من السيرفر
  if os.path.exists(input_path):
    os.remove(input_path)
  if os.path.exists(output_path):
    os.remove(output_path)


if __name__ == "__main__":
  app = ApplicationBuilder().token(TOKEN).build()

  # التعامل مع أي ملف يتم إرساله للبوت
  app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

  print("البوت يعمل الآن ويستمع للملفات...")
  app.run_polling()
