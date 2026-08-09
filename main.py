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

API_TOKEN = '1971050276:AAGMnosyWdq58EzSxHudHxZ3RtbT_34t_mc'  
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# قاموس مؤقت لحفظ حالة المستخدمين بدقة لتجنب مشاكل الـ FSM
user_sessions = {}

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
        types.InlineKeyboardButton("2️⃣ MASS (فحص جماعي بدون بروكسي)", callback_data="ch_mass_proxyless"),
        types.InlineKeyboardButton("3️⃣ BACK (رجوع)", callback_data="go_back")
    )
    return kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_sessions[message.from_user.id] = {'step': 'main'}
    await message.answer(
        "⚡ **مرحباً بك يا إنستا في لوحة التحكم:**\nاختر أحد الأقسام الرئيسية للبدء:",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == 'menu_checker')
async def cb_checker(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("📂 **قائمة الـ CHECKER:**\nاختر خيار الفحص:", reply_markup=get_checker_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'go_back')
async def cb_back(call: types.CallbackQuery):
    await call.answer()
    user_sessions[call.from_user.id] = {'step': 'main'}
    await call.message.edit_text("⚡ لوحة التحكم الرئيسية:", reply_markup=get_main_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'exit_bot')
async def cb_exit(call: types.CallbackQuery):
    await call.answer("تم الإغلاق")
    user_sessions[call.from_user.id] = {'step': 'closed'}
    await call.message.edit_text("❌ تم إغلاق لوحة التحكم. اضغط /start لإعادة التشغيل.")

# عند اختيار الفحص الجماعي بدون بروكسي
@dp.callback_query_handler(lambda c: c.data == 'ch_mass_proxyless')
async def cb_ch_mass_proxyless(call: types.CallbackQuery):
    await call.answer()
    user_sessions[call.from_user.id] = {'step': 'waiting_cards_file'}
    await call.message.edit_text("📁 أرسل الآن **ملف البطاقات (.txt)** للفحص (بدون بروكسي).")

# استقبال أي ملف مستند (Document) وفحص الخطوة الحالية بناءً على القاموس الآمن
@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_incoming_documents(message: types.Message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id, {'step': 'main'})
    step = session.get('step')

    # الخطوة الأولى: استقبال ملف البطاقات
    if step == 'waiting_cards_file':
        try:
            cc_path = f"cards_{user_id}.txt"
            await message.document.download(destination_file=cc_path)
            
            # تحديث الجلسة للانتقال لطلب ملف الروابط فوراً
            user_sessions[user_id] = {'step': 'waiting_sites_file', 'cc_file': cc_path}
            
            await message.answer(
                "✅ **تم استلام ملف البطاقات بنجاح.**\n\n"
                "📂 الآن أرسل **ملف المواقع أو الروابط (.txt)** للفحص عليها جماعياً:"
            )
        except Exception as e:
            await message.answer(f"❌ حدث خطأ أثناء تحميل ملف البطاقات: {str(e)}")
            user_sessions[user_id] = {'step': 'main'}

    # الخطوة الثانية: استقبال ملف الروابط وبدء العمليات
    elif step == 'waiting_sites_file':
        try:
            site_path = f"sites_{user_id}.txt"
            await message.document.download(destination_file=site_path)
            
            cc_file = session.get('cc_file')
            cards = []
            if cc_file and os.path.exists(cc_file):
                with open(cc_file, 'r', encoding='utf-8', errors='ignore') as f:
                    cards = [line.strip() for line in f.read().splitlines() if line.strip() and '|' in line]
                    
            sites = []
            if os.path.exists(site_path):
                with open(site_path, 'r', encoding='utf-8', errors='ignore') as f:
                    sites = [line.strip() for line in f.read().splitlines() if line.strip()]
                
            if not cards or not sites:
                await message.answer(f"❌ خطأ: ملف البطاقات ({len(cards)}) أو ملف الروابط ({len(sites)}) فارغ أو تالف!")
                user_sessions[user_id] = {'step': 'main'}
                return
                
            await message.answer(f"🚀 **تم استلام ملف الروابط بنجاح تام!**\n- عدد البطاقات: {len(cards)}\n- عدد المواقع: {len(sites)}\n\nجاري بدء الفحص التجريبي...")
            
            valid_count = 0
            dead_count = 0
            target_site = sites[0]
            if not target_site.startswith('http'):
                target_site = 'https://' + target_site
                
            for line in cards[:2]:
                parts = parse_cc_string(line)
                if parts:
                    success, res_msg, gateway, price, currency = await process_card(
                        parts['cc'], parts['mes'], parts['ano'], parts['cvv'], target_site, None, None
                    )
                    clean = extract_clean_response(res_msg)
                    if success:
                        valid_count += 1
                        await message.answer(f"✅ **مقبولة:** `{line}`\n- الرد: {clean}")
                    else:
                        dead_count += 1
                        
            await message.answer(f"📊 **نتائج التجربة:**\n- الموقع: {target_site}\n- المقبولة: {valid_count}\n- المرفوضة: {dead_count}")

        except Exception as e:
            await message.answer(f"❌ حدث خطأ تقني: {str(e)}")
        finally:
                    user_sessions[user_id] = {'step': 'main'}
                    await message.answer("⚡ اضغط /start للعودة إلى القائمة الرئيسية.")
    else:
        await message.answer("⚠️ يرجى اختيار القسم المناسب من القائمة أولاً أو اضغط /start للبدء.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
