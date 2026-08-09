import logging
import os
import sys
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api import process_card, parse_cc_string, extract_clean_response, fetch_products

# ضع توكن البوت الخاص بك هنا
API_TOKEN = '5799226531:AAGY9ve702AFllrVQetQnIKjM2olGJIjDU8'  
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# حالات FSM لتتبع خطوات المدخلات للبوت
class BotStates(StatesGroup):
    waiting_single_cc = State()
    waiting_single_site = State()
    
    waiting_mass_proxy_file = State()
    waiting_mass_cc_file = State()
    waiting_mass_site_input = State()
    
    waiting_site_single = State()
    waiting_site_file = State()

# --- لوحات المفاتيح (الـ 13 خياراً كأزرار تليجرام) ---

def get_main_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("1️⃣ CHECKER", callback_data="menu_checker"),
        types.InlineKeyboardButton("2️⃣ SITE", callback_data="menu_site")
    )
    kb.add(types.InlineKeyboardButton("3️⃣ EXIT", callback_data="exit_bot"))
    return kb

def get_checker_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("1️⃣ SINGLE (فحص فردي)", callback_data="ch_single"),
        types.InlineKeyboardButton("2️⃣ MASS (فحص جماعي)", callback_data="ch_mass"),
        types.InlineKeyboardButton("3️⃣ BACK (رجوع)", callback_data="go_back")
    )
    return kb

def get_site_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("1️⃣ SINGLE (موقع فردي)", callback_data="st_single"),
        types.InlineKeyboardButton("2️⃣ MASS (مواقع جماعي)", callback_data="st_mass"),
        types.InlineKeyboardButton("3️⃣ BACK (رجوع)", callback_data="go_back")
    )
    return kb

def get_proxy_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("1️⃣ HTTP/S", callback_data="proxy_1"),
        types.InlineKeyboardButton("2️⃣ SOCKS4", callback_data="proxy_2"),
        types.InlineKeyboardButton("3️⃣ SOCKS5", callback_data="proxy_3"),
        types.InlineKeyboardButton("4️⃣ PROXYLESS", callback_data="proxy_4")
    )
    return kb


# --- معالجة الأوامر والقوائم ---

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "⚡ **مرحباً بك يا إنستا في لوحة التحكم:**\nاختر أحد الأقسام الرئيسية للبدء:",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == 'menu_checker')
async def cb_checker(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("📂 **قائمة الـ CHECKER:**\nاختر خيار الفحص:", reply_markup=get_checker_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'menu_site')
async def cb_site(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("🌐 **قائمة الـ SITE:**\nاختر خيار فحص المواقع:", reply_markup=get_site_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'go_back')
async def cb_back(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("⚡ لوحة التحكم الرئيسية:", reply_markup=get_main_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'exit_bot')
async def cb_exit(call: types.CallbackQuery):
    await call.answer("تم الإغلاق")
    await call.message.edit_text("❌ تم إغلاق لوحة التحكم. اضغط /start لإعادة التشغيل.")


# ---------------------------------------------------------
# 1. قسم CHECKER - الفحص الفردي (Single)
# ---------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == 'ch_single')
async def cb_ch_single(call: types.CallbackQuery):
    await call.answer()
    await BotStates.waiting_single_cc.set()
    await call.message.answer("💳 أرسل بيانات البطاقة بهذا التنسيق:\n`card|mes|ano|cvv`")

@dp.message_handler(state=BotStates.waiting_single_cc)
async def get_single_cc(message: types.Message, state: FSMContext):
    await state.update_data(cc_string=message.text.strip())
    await BotStates.waiting_single_site.set()
    await message.answer("🌐 أرسل الآن رابط الموقع المراد الفحص عليه:")

@dp.message_handler(state=BotStates.waiting_single_site)
async def get_single_site_and_run(message: types.Message, state: FSMContext):
    site = message.text.strip()
    if not site.startswith('http'):
        site = 'https://' + site
        
    data = await state.get_data()
    cc_string = data.get('cc_string')
    
    await message.answer("🔄 جاري فحص البطاقة...")
    try:
        parts = parse_cc_string(cc_string)
        success, res_msg, gateway, price, currency = await process_card(
            parts['cc'], parts['mes'], parts['ano'], parts['cvv'], site, None, None
        )
        clean = extract_clean_response(res_msg)
        await message.answer(f"✅ **النتيجة:**\n- الحالة: {'مقبولة' if success else 'مرفوضة'}\n- الرد: {clean}\n- السعر: {price} {currency}")
    except Exception as e:
        await message.answer(f"❌ حدث خطأ: {str(e)}")
        
    await state.finish()
    await message.answer("اختر من القائمة الرئيسية:", reply_markup=get_main_keyboard())


# ---------------------------------------------------------
# 2. قسم CHECKER - الفحص الجماعي (Mass) + خيارات البروكسي (4)
# ---------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == 'ch_mass')
async def cb_ch_mass(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("⚙️ **اختر نوع البروكسي للفحص الجماعي:**", reply_markup=get_proxy_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith('proxy_'))
async def cb_proxy_choice(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    proxy_type = call.data.split('_')[1]
    await state.update_data(proxy_type=int(proxy_type))
    
    if proxy_type == '4': # Proxyless
        await BotStates.waiting_mass_cc_file.set()
        await call.message.edit_text("📁 أرسل الآن **ملف البطاقات (.txt)** للفحص (بدون بروكسي).")
    else:
        await BotStates.waiting_mass_proxy_file.set()
        await call.message.edit_text("📁 أرسل أولاً **ملف البروكسي (.txt)**.")

@dp.message_handler(state=BotStates.waiting_mass_proxy_file, content_types=types.ContentTypes.DOCUMENT)
async def get_proxy_doc(message: types.Message, state: FSMContext):
    doc = message.document
    file = await bot.get_file(doc.file_id)
    proxy_path = f"proxy_{message.from_user.id}.txt"
    await file.download(destination_file=proxy_path)
    
    await state.update_data(proxy_file=proxy_path)
    await BotStates.waiting_mass_cc_file.set()
    await message.answer("✅ تم استلام ملف البروكسي.\nالآن أرسل **ملف البطاقات (.txt)**.")

@dp.message_handler(state=BotStates.waiting_mass_cc_file, content_types=types.ContentTypes.DOCUMENT)
async def get_cc_doc(message: types.Message, state: FSMContext):
    doc = message.document
    file = await bot.get_file(doc.file_id)
    cc_path = f"cards_{message.from_user.id}.txt"
    await file.download(destination_file=cc_path)
    
    await state.update_data(cc_file=cc_path)
    await BotStates.waiting_mass_site_input.set()
    await message.answer("🌐 أرسل رابط الموقع أو أرسل ملف `.txt` للمواقع للفحص عليها.")

@dp.message_handler(state=BotStates.waiting_mass_site_input)
async def run_mass_checker(message: types.Message, state: FSMContext):
    await message.answer("🚀 تم استلام كافة المتطلبات وجاري بدء الفحص الجماعي في الخلفية...")
    await state.finish()
    await message.answer("اختر من القائمة الرئيسية:", reply_markup=get_main_keyboard())


# ---------------------------------------------------------
# 3. قسم SITE - فحص المواقع (فردي وجماعي)
# ---------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == 'st_single')
async def cb_st_single(call: types.CallbackQuery):
    await call.answer()
    await BotStates.waiting_site_single.set()
    await call.message.answer("🌐 أرسل رابط الموقع المراد فحصه:")

@dp.message_handler(state=BotStates.waiting_site_single)
async def run_site_single(message: types.Message, state: FSMContext):
    site = message.text.strip()
    await message.answer(f"🔍 جاري فحص الموقع: {site} باستخدام بطاقات الاختبار...")
    await state.finish()
    await message.answer("اختر من القائمة الرئيسية:", reply_markup=get_main_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'st_mass')
async def cb_st_mass(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("📁 أرسل ملف `.txt` يحتوي على قائمة المواقع للفحص الجماعي.")

@dp.message_handler(state=BotStates.waiting_site_file, content_types=types.ContentTypes.DOCUMENT)
async def run_site_mass(message: types.Message, state: FSMContext):
    doc = message.document
    file = await bot.get_file(doc.file_id)
    site_path = f"sites_{message.from_user.id}.txt"
    await file.download(destination_file=site_path)
    
    await message.answer("🚀 تم استلام ملف المواقع وجارٍ فحصها...")
    await state.finish()
    await message.answer("اختر من القائمة الرئيسية:", reply_markup=get_main_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
