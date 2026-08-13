import asyncio
import concurrent.futures
import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ضع توكن البوت الخاص بك هنا
TOKEN = "8424469694:AAHGrmgmFVc0XaxCz0O2uEYtJWsEn4CoknU"

TEST_URL = "https://httpbin.org/ip"
TIMEOUT = 5


def check_proxy(proxy):
    proxy_url = proxy if "://" in proxy else f"http://{proxy}"
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            ip_data = response.json().get("origin", "مخفي")
            return proxy, True, ip_data
    except requests.exceptions.RequestException:
        pass
    return proxy, False, None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك! أرسل ملف `.txt` يحتوي على البروكسيات وسأقوم بفحصها وعرض لوحة النتائج المباشرة."
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document.file_name.endswith(".txt"):
        await update.message.reply_text("الرجاء إرسال ملف بصيغة .txt فقط.")
        return

    status_msg = await update.message.reply_text(
        "⏳ جاري تحميل الملف وتحضير لوحة الفحص..."
    )

    file = await context.bot.get_file(document.file_id)
    input_path = f"input_{update.effective_user.id}.txt"
    output_path = f"live_{update.effective_user.id}.txt"

    await file.download_to_drive(input_path)

    with open(input_path, "r", encoding="utf-8") as f:
        proxies_list = [line.strip() for line in f if line.strip()]

    if not proxies_list:
        await status_msg.edit_text("الملف فارغ!")
        if os.path.exists(input_path):
            os.remove(input_path)
        return

    total = len(proxies_list)
    await status_msg.edit_text(
        f"📊 **لوحة الفحص المباشر**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"▪️ إجمالي البروكسيات: {total}\n"
        f"▪️ الحالة: جاري الفحص الآن... 🔄"
    )

    # تشغيل الفحص
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [
            loop.run_in_executor(executor, check_proxy, p) for p in proxies_list
        ]
        results = await asyncio.gather(*futures)

    live_proxies = []
    dead_count = 0
    live_details = []

    for proxy, is_live, ip in results:
        if is_live:
            live_proxies.append(proxy)
            live_details.append(f"✅ `{proxy}` (IP: {ip})")
        else:
            dead_count += 1

    # حفظ البروكسيات الحية في ملف
    with open(output_path, "w", encoding="utf-8") as f:
        for p in live_proxies:
            f.write(f"{p}\n")

    # إنشاء لوحة النتائج النهائية داخل رسالة البوت
    live_text = (
        "\n".join(live_details[:15]) if live_details else "لا توجد بروكسيات حية"
    )
    if len(live_details) > 15:
        live_text += f"\n... و {len(live_details) - 15} بروكسيات أخرى."

    report_text = (
        f"📊 **لوحة نتائج الفحص النهائية**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📁 اسم الملف: `{document.file_name}`\n"
        f"🌐 إجمالي المفحوص: `{total}`\n"
        f"🟢 البروكسيات الشغالة: `{len(live_proxies)}`\n"
        f"🔴 البروكسيات الميتة: `{dead_count}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💡 **عينة من الشغال:**\n{live_text}"
    )

    await status_msg.edit_text(report_text, parse_mode="Markdown")

    # إرسال الملف الكامل للنتيجة
    if live_proxies:
        with open(output_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename="live_proxies.txt",
                caption="📄 تفضل ملف البروكسيات الشغالة كاملة.",
            )

    # تنظيف الملفات المؤقتة
    for path in [input_path, output_path]:
        if os.path.exists(path):
            os.remove(path)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("البوت يعمل الآن...")
    app.run_polling()
