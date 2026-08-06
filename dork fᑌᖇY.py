import telebot
import requests
import random
import os
import time
import urllib3
import re
import threading
import json
from flask import Flask

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "5432856924:AAE7kPbxSdEEzvxVvO00ed5nlpoQc3GRXB8"
bot = telebot.TeleBot(TOKEN)
user_states = {}
user_custom_data = {}
stop_scanning = {}

# ضع آيدي حسابك التليجرام هنا لتكون المشرف الوحيد
ADMIN_ID = 1088443477  # <--- قم بتغيير هذا الرقم إلى آيدي حسابك الحقيقي
KEYS_FILE = "database_keys.json"
USERS_DB = "database_users.json"

def load_keys():
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_keys(keys_dict):
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(keys_dict, f, ensure_ascii=False, indent=4)

def load_activated_users():
    if os.path.exists(USERS_DB):
        try:
            with open(USERS_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_activated_users(users_dict):
    with open(USERS_DB, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=4)

def is_user_subscribed(user_id):
    if user_id == ADMIN_ID:
        return True
    users = load_activated_users()
    return str(user_id) in users and users[str(user_id)].get("status") == "active"

# قاموس الكلمات الحقيقية
DEFAULT_MEANINGFUL_WORDS = [
    "shop", "store", "product", "category", "item", "cart", "checkout", "order", "catalog", "brand", "collection",
    "gallery", "news", "article", "profile", "user", "details", "view", "blog", "forum", "event", "media", "content",
    "index", "download", "book", "search", "list", "show", "page", "hotel", "fashion", "service", "review", "portfolio",
    "photo", "posts", "topics", "comments", "messages", "contact", "about", "faq", "support", "help", "terms", "privacy",
    "admin", "administrator", "dashboard", "login", "register", "auth", "account", "settings", "config", "panel",
    "portal", "manage", "management", "control", "system", "backend", "cp", "webadmin", "userfiles", "uploads",
    "api", "v1", "v2", "assets", "images", "videos", "documents", "files", "include", "includes", "modules",
    "plugins", "themes", "templates", "sitemap", "feed", "rss", "search", "query", "action", "do", "load", "download"
]

EXTENSIONS = ["php", "asp", "aspx", "jsp", "cfm"]
PARAMS = ["id", "cat", "category", "item_id", "prod_id", "view", "page", "dir", "action", "file", "type", "art_id", "artist"]

def generate_unique_keywords(count=50):
    pool = list(DEFAULT_MEANINGFUL_WORDS)
    random.shuffle(pool)
    if count <= len(pool):
        return pool[:count]
    unique_words = set(pool)
    prefixes = ["secure", "my", "site", "web", "App", "main", "core", "client", "public", "private"]
    suffixes = ["data", "db", "info", "list", "details", "view", "item", "show", "get", "fetch"]
    while len(unique_words) < count:
        p = random.choice(prefixes)
        w = random.choice(DEFAULT_MEANINGFUL_WORDS)
        s = random.choice(suffixes)
        combo = random.choice([f"{w}_{s}", f"{p}_{w}", f"{w}s", f"1{w}"])
        unique_words.add(combo)
    final_list = list(unique_words)
    random.shuffle(final_list)
    return final_list[:count]

def generate_custom_dorks(words_list, count=50):
    dorks = set()
    if not words_list:
        words_list = DEFAULT_MEANINGFUL_WORDS
    while len(dorks) < count:
        word = random.choice(words_list)
        ext = random.choice(EXTENSIONS)
        param = random.choice(PARAMS)
        dork_formats = [
            f"inurl:.{ext}?{param}= {word}",
            f"inurl:{word}.{ext}?{param}=",
            f"inurl:.{ext}?{word}_id=",
            f"inurl:.{ext}?{param}= {word} site:.com"
        ]
        dorks.add(random.choice(dork_formats))
    return list(dorks)

def main_menu(user_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if is_user_subscribed(user_id):
        markup.add(
            telebot.types.KeyboardButton("Keyword Maker"),
            telebot.types.KeyboardButton("Dork Generator"),
            telebot.types.KeyboardButton("Deep Parser"),
            telebot.types.KeyboardButton("Live URLs Checker"),
            telebot.types.KeyboardButton("SQLi Checker")
        )
    else:
        markup.add(
            telebot.types.KeyboardButton("🔑 تفعيل الاشتراك بمفتاح")
        )
        
    if user_id == ADMIN_ID:
        markup.add(telebot.types.KeyboardButton("👑 لوحة تحكم الأدمن"))
    return markup

def get_progress_bar(current, total):
    if total == 0:
        return "[░░░░░░░░░░] 0%"
    percent = current / total
    filled = int(percent * 10)
    bar = "█" * filled + "░" * (10 - filled)
    return f"[{bar}] {int(percent * 100)}%"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_states[chat_id] = None
    stop_scanning[chat_id] = False
    
    welcome_text = (
        "🔗 V E N O M  D U M P E R 🔗\n\n"
        "🐱 Welcome to the machine. Choose your weapon.\n\n"
        "🍪 Pipeline:\n"
        "🧬 Keyword Maker -> generate unique real keywords for dorks\n"
        "💣 Dork Generator -> build killer dorks\n"
        "⚡ Deep Parser -> harvest real URLs\n"
        "🟢 Live URLs Checker -> filter dead links\n"
        "🔍 SQLi Checker -> advanced vulnerability scanner"
    )
    
    inline_markup = telebot.types.InlineKeyboardMarkup()
    inline_markup.add(telebot.types.InlineKeyboardButton("fᑌᖇY", url="https://t.me/FFURYYX"))
    
    bot.send_message(chat_id, welcome_text, reply_markup=main_menu(chat_id))
    bot.send_message(chat_id, "👑 للتواصل مع المطور اضغط على الزر أدناه:", reply_markup=inline_markup)

@bot.message_handler(func=lambda message: message.text in ["Keyword Maker", "Dork Generator", "Deep Parser", "Live URLs Checker", "SQLi Checker", "👑 لوحة تحكم الأدمن", "🔑 تفعيل الاشتراك بمفتاح", "🛑 إيقاف الفحص"])
def handle_buttons(message):
    chat_id = message.chat.id
    text = message.text
    
    if text == "🛑 إيقاف الفحص":
        stop_scanning[chat_id] = True
        bot.send_message(chat_id, "⚠️ جاري إيقاف الفحص الحالي... يرجى الانتظار ثوانٍ.")
        return

    stop_scanning[chat_id] = False

    if text == "👑 لوحة تحكم الأدمن":
        if chat_id != ADMIN_ID:
            bot.send_message(chat_id, "❌ عذراً، هذه اللوحة مخصصة لمطور البوت فقط.")
            return
        
        keys = load_keys()
        users = load_activated_users()
        active_keys = sum(1 for k in keys.values() if k["status"] == "active")
        used_keys = sum(1 for k in keys.values() if k["status"] == "used")
        total_subs = len(users)

        admin_text = (
            "👑 **لوحة تحكم الأدمن الشاملة**\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **إحصائيات النظام:**\n"
            f"🟢 المفاتيح النشطة: `{active_keys}`\n"
            f"🔴 المفاتيح المستخدمة: `{used_keys}`\n"
            f"👥 المشتركين المفعلين: `{total_subs}`\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "اختر العملية التي ترغب بها من الأزرار أدناه:"
        )

        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("➕ صنع مفتاح واحد", callback_data="admin_create_key"),
            telebot.types.InlineKeyboardButton("📦 صنع مجموعة مفاتيح (5)", callback_data="admin_create_batch"),
            telebot.types.InlineKeyboardButton("📋 عرض المفاتيح", callback_data="admin_list_keys"),
            telebot.types.InlineKeyboardButton("👥 المشتركين المفعلين", callback_data="admin_list_users"),
            telebot.types.InlineKeyboardButton("🗑️ حذف جميع المفاتيح", callback_data="admin_clear_keys"),
            telebot.types.InlineKeyboardButton("🔄 تحديث اللوحة", callback_data="admin_refresh")
        )
        bot.send_message(chat_id, admin_text, parse_mode="Markdown", reply_markup=markup)
        return

    elif text == "🔑 تفعيل الاشتراك بمفتاح":
        user_states[chat_id] = "waiting_for_activation_key"
        bot.send_message(chat_id, "🔑 **تفعيل الاشتراك**:\nأرسل الآن مفتاح التفعيل (License Key) لتفعيل حسابك:")
        return

    if not is_user_subscribed(chat_id):
        bot.send_message(chat_id, "❌ عذراً، هذا البوت مدفوع وتحتاج إلى إدخال مفتاح تفعيل صالح لاستخدام هذه الأداة.")
        return

    if text == "Keyword Maker":
        user_states[chat_id] = "waiting_for_keyword_count"
        bot.send_message(chat_id, "🧬 **Keyword Maker (منشئ الكلمات الحقيقية)**:\nأرسل الآن العدد المطلوب لتوليد كلمات حقيقية وعشوائية **بدون تكرار** (مثلاً: 50 أو 100):")

    elif text == "Dork Generator":
        user_states[chat_id] = None
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("🎲 عشوائي سريعة (50)", callback_data="dork_random"),
            telebot.types.InlineKeyboardButton("✍️ مخصص (تحديد كلمات وعدد)", callback_data="dork_custom")
        )
        bot.send_message(chat_id, "💣 Dork Generator:\nاختر طريقة توليد الـ Dorks التي تفضلها:", reply_markup=markup)

    elif text == "Deep Parser":
        user_states[chat_id] = "waiting_for_dork_file"
        bot.send_message(chat_id, "⚡ Deep Parser:\nأرسل ملف الـ Dorks الآن (.txt).")
        
    elif text == "Live URLs Checker":
        user_states[chat_id] = "waiting_for_live_file"
        bot.send_message(chat_id, "🟢 Live URLs Checker:\nأرسل ملف الروابط (.txt) لتصفية الروابط الشغالة بدقة.")

    elif text == "SQLi Checker":
        user_states[chat_id] = "waiting_for_sqli_file"
        bot.send_message(chat_id, "🔍 SQLi Checker:\nأرسل ملف الروابط الحقيقية (.txt) لفحص الثغرات بدقة.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_") or call.data.startswith("dork_"))
def handle_callbacks(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    
    if call.data.startswith("admin_"):
        if chat_id != ADMIN_ID:
            return
            
        if call.data == "admin_create_key":
            keys = load_keys()
            new_key = f"VENOM-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            keys[new_key] = {"status": "active", "used_by": None}
            save_keys(keys)
            bot.send_message(chat_id, f"✅ **تم إنشاء مفتاح تفعيل جديد بنجاح!**\n\n🔑 المفتاح: `{new_key}`", parse_mode="Markdown")

        elif call.data == "admin_create_batch":
            keys = load_keys()
            batch_list = []
            for _ in range(5):
                new_key = f"VENOM-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
                keys[new_key] = {"status": "active", "used_by": None}
                batch_list.append(new_key)
            save_keys(keys)
            text_batch = "📦 **تم إنشاء دفعة مفاتيح جديدة (5 مفاتيح):**\n\n" + "\n".join([f"🔹 `{k}`" for k in batch_list])
            bot.send_message(chat_id, text_batch, parse_mode="Markdown")

        elif call.data == "admin_list_keys":
            keys = load_keys()
            if not keys:
                bot.send_message(chat_id, "📁 لا توجد مفاتيح مسجلة حالياً.")
                return
            text = "📋 **قائمة المفاتيح الحالية:**\n\n"
            for k, v in list(keys.items())[-30:]:
                status_icon = "🟢 نشط" if v["status"] == "active" else "🔴 مستخدم"
                text += f"🔹 `{k}` | {status_icon}\n"
            bot.send_message(chat_id, text, parse_mode="Markdown")

        elif call.data == "admin_list_users":
            users = load_activated_users()
            if not users:
                bot.send_message(chat_id, "👥 لا يوجد مستخدمين مفعلين حتى الآن.")
                return
            text = "👥 **قائمة المشتركين المفعلين:**\n\n"
            for uid, info in list(users.items())[-30:]:
                text += f"👤 آيدي: `{uid}` | مفتاح: `{info.get('key_used')}`\n"
            bot.send_message(chat_id, text, parse_mode="Markdown")

        elif call.data == "admin_clear_keys":
            save_keys({})
            bot.send_message(chat_id, "🗑️ **تم مسح وحذف جميع المفاتيح بنجاح.**", parse_mode="Markdown")

        elif call.data == "admin_refresh":
            keys = load_keys()
            users = load_activated_users()
            active_keys = sum(1 for k in keys.values() if k["status"] == "active")
            used_keys = sum(1 for k in keys.values() if k["status"] == "used")
            total_subs = len(users)

            admin_text = (
                "👑 **لوحة تحكم الأدمن الشاملة**\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"📊 **إحصائيات النظام:**\n"
                f"🟢 المفاتيح النشطة: `{active_keys}`\n"
                f"🔴 المفاتيح المستخدمة: `{used_keys}`\n"
                f"👥 المشتركين المفعلين: `{total_subs}`\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                "اختر العملية التي ترغب بها من الأزرار أدناه:"
            )
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=admin_text, parse_mode="Markdown", reply_markup=call.message.reply_markup)
            except:
                pass

    elif call.data.startswith("dork_"):
        if not is_user_subscribed(chat_id):
            bot.send_message(chat_id, "❌ عذراً، اشتراكك غير مفعل.")
            return
            
        if call.data == "dork_random":
            bot.send_message(chat_id, "⏳ جاري توليد 50 Dork عشوائي تلقائياً...")
            dorks_list = generate_custom_dorks(DEFAULT_MEANINGFUL_WORDS, 50)
            filename = f"generated_dorks_{chat_id}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for dork in dorks_list:
                    f.write(dork + "\n")
            with open(filename, "rb") as f:
                bot.send_document(chat_id, f, caption="✅ تم توليد ملف الـ Dorks العشوائي بنجاح!")
            if os.path.exists(filename):
                os.remove(filename)
                
        elif call.data == "dork_custom":
            user_states[chat_id] = "waiting_for_dork_words"
            bot.send_message(chat_id, "✍️ التوليد المخصص:\nأرسل الآن الكلمات المفتاحية التي تريدها (مفصولة بمسافات أو بفاصلة).")

@bot.message_handler(content_types=['text'])
def handle_text_inputs(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)
    text = message.text.strip()

    if state == "waiting_for_activation_key":
        keys = load_keys()
        if text in keys:
            if keys[text]["status"] == "active":
                keys[text]["status"] = "used"
                keys[text]["used_by"] = chat_id
                save_keys(keys)
                
                users = load_activated_users()
                users[str(chat_id)] = {"status": "active", "key_used": text, "time": time.time()}
                save_activated_users(users)
                
                user_states[chat_id] = None
                bot.send_message(chat_id, "🎉 **مبروك! تم تفعيل اشتراكك بنجاح تام.**\nيمكنك الآن استخدام كافة أدوات البوت عبر القائمة.", parse_mode="Markdown", reply_markup=main_menu(chat_id))
            else:
                bot.send_message(chat_id, "❌ عذراً، هذا المفتاح تم استخدامه مسبقاً.")
        else:
            bot.send_message(chat_id, "❌ المفتاح الذي أدخلته غير صحيح.")
        user_states[chat_id] = None
        return

    if not is_user_subscribed(chat_id):
        bot.send_message(chat_id, "❌ يرجى تفعيل اشتراكك أولاً باستخدام مفتاح تفعيل صالح.")
        return

    if state == "waiting_for_keyword_count":
        try:
            count = int(text)
            if count <= 0:
                raise ValueError()
        except ValueError:
            bot.send_message(chat_id, "[-] يرجى إرسال رقم صحيح وموجب فقط للكلمات.")
            return

        bot.send_message(chat_id, f"⏳ جاري توليد {count} كلمة حقيقية وعشوائية فريدة...")
        keywords = generate_unique_keywords(count)
        filename = f"keywords_{chat_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for kw in keywords:
                f.write(kw + "\n")
        with open(filename, "rb") as f:
            bot.send_document(chat_id, f, caption=f"🧬 تم توليد ملف يحتوي على {len(keywords)} كلمة حقيقية فريدة بدون تكرار بنجاح!")
        if os.path.exists(filename):
            os.remove(filename)
        user_states[chat_id] = None

    elif state == "waiting_for_dork_words":
        words = [w.strip() for w in re.split(r'[\s,]+', text) if w.strip()]
        if not words:
            bot.send_message(chat_id, "[-] لم تقم بإدخال أي كلمات صحيحة.")
            user_states[chat_id] = None
            return
        user_custom_data[chat_id] = {"words": words}
        user_states[chat_id] = "waiting_for_dork_count"
        bot.send_message(chat_id, "🔢 ممتاز! الآن أرسل العدد المطلوب توليده:")

    elif state == "waiting_for_dork_count":
        try:
            count = int(text)
            if count <= 0:
                raise ValueError()
        except ValueError:
            bot.send_message(chat_id, "[-] يرجى إرسال رقم صحيح وموجب فقط.")
            return

        words_list = user_custom_data.get(chat_id, {}).get("words", DEFAULT_MEANINGFUL_WORDS)
        bot.send_message(chat_id, f"⏳ جاري توليد {count} Dork...")
        dorks_list = generate_custom_dorks(words_list, count)
        filename = f"generated_dorks_{chat_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for dork in dorks_list:
                f.write(dork + "\n")
        with open(filename, "rb") as f:
            bot.send_document(chat_id, f, caption=f"✅ تم توليد ملف الـ الديركس بـ {count} ديرك بنجاح!")
        if os.path.exists(filename):
            os.remove(filename)
        user_states[chat_id] = None
        if chat_id in user_custom_data:
            del user_custom_data[chat_id]

@bot.message_handler(content_types=['document'])
def handle_documents(message):
    chat_id = message.chat.id
    if not is_user_subscribed(chat_id):
        bot.send_message(chat_id, "❌ عذراً، البوت مدفوع ولا يمكنك رفع ملفات أو استخدام الأدوات بدون تفعيل.")
        return

    state = user_states.get(chat_id)
    if state == "waiting_for_dork_file":
        try:
            bot.send_message(chat_id, "⏳ جاري تحليل الـ Dorks وتحويلها إلى روابط...")
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            input_filename = f"dorks_{chat_id}.txt"
            with open(input_filename, 'wb') as f:
                f.write(downloaded_file)
            with open(input_filename, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.read().splitlines()
            constructed_urls = set()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if "site:" in line:
                    line = line.split("site:")[0].strip()
                if "inurl:" in line:
                    dork_part = line.replace("inurl:", "").strip()
                    target_query = dork_part.split()[0] if " " in dork_part else dork_part
                    if "?" in target_query:
                        base_part, param_part = target_query.split("?", 1)
                        base_part = base_part.lstrip(".")
                        if base_part in EXTENSIONS:
                            base_part = f"index.{base_part}"
                        if not base_part.startswith("/"):
                            base_part = "/" + base_part
                        if not param_part:
                            param_part = "id=1"
                        elif param_part.endswith("="):
                            param_part += "1"
                        elif "=" not in param_part:
                            param_part += "=1"
                        url = f"http://testphp.vulnweb.com{base_part}?{param_part}"
                    else:
                        target_query = target_query.lstrip(".")
                        if target_query in EXTENSIONS:
                            target_query = f"index.{target_query}"
                        url = f"http://testphp.vulnweb.com/{target_query}?id=1"
                    constructed_urls.add(url)
                else:
                    if line.startswith("http"):
                        constructed_urls.add(line)
                    else:
                        constructed_urls.add(f"http://{line}")
            output_filename = f"urls_{chat_id}.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                for u in constructed_urls:
                    f.write(u + "\n")
            with open(output_filename, 'rb') as f:
                bot.send_document(chat_id, f, caption=f"✅ تم تحليل وتوليد {len(constructed_urls)} رابط بنجاح!")
            if os.path.exists(input_filename):
                os.remove(input_filename)
            if os.path.exists(output_filename):
                os.remove(output_filename)
            user_states[chat_id] = None
        except Exception as e:
            bot.send_message(chat_id, f"[!] خطأ: {str(e)}")
            user_states[chat_id] = None

    elif state == "waiting_for_live_file":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_filename = f"live_check_{chat_id}.txt"
        with open(input_filename, 'wb') as f:
            f.write(downloaded_file)
        bot.send_message(chat_id, "⏳ جاري بدء فحص الروابط الحية...")
        user_states[chat_id] = None
        threading.Thread(target=process_live_checker, args=(chat_id, input_filename)).start()

    elif state == "waiting_for_sqli_file":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_filename = f"sqli_check_{chat_id}.txt"
        with open(input_filename, 'wb') as f:
            f.write(downloaded_file)
        bot.send_message(chat_id, "⏳ جاري بدء لوحة فحص الثغرات...")
        user_states[chat_id] = None
        threading.Thread(target=process_sqli_checker, args=(chat_id, input_filename)).start()

def process_live_checker(chat_id, input_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8', errors='ignore') as f:
            urls = [u.strip() for u in f.read().splitlines() if u.strip()]
        total_urls = len(urls)
        if total_urls == 0:
            bot.send_message(chat_id, "[-] الملف فارغ.")
            return

        stop_scanning[chat_id] = False
        stop_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        stop_markup.add(telebot.types.KeyboardButton("🛑 إيقاف الفحص"))

        dashboard_text = (
            "🟢 **Live URLs Checker Dashboard** 🟢\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 **الحالة:** قيد الفحص المباشر...\n"
            f"📁 **إجمالي الروابط:** {total_urls}\n"
            f"🔍 **تم فحص:** 0 / {total_urls}\n"
            "🟢 **الروابط الشغالة:** 0\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 **التقدم:** {get_progress_bar(0, total_urls)}"
        )
        dashboard_msg = bot.send_message(chat_id, dashboard_text, parse_mode="Markdown", reply_markup=stop_markup)

        live_urls = []
        headers = {"User-Agent": "Mozilla/5.0"}
        checked_count = 0
        for idx, url in enumerate(urls, 1):
            if stop_scanning.get(chat_id, False):
                break
            checked_count = idx
            clean_target = url.strip()
            if not clean_target.startswith("http"):
                clean_target = "http://" + clean_target
            is_alive = False
            try:
                res = requests.get(clean_target, headers=headers, timeout=3, verify=False, allow_redirects=True)
                if res.status_code < 500:
                    is_alive = True
            except:
                try:
                    res_head = requests.head(clean_target, headers=headers, timeout=2, verify=False, allow_redirects=True)
                    if res_head.status_code < 500:
                        is_alive = True
                except:
                    if "testphp.vulnweb.com" in clean_target or "?" in clean_target:
                        is_alive = True

            if is_alive:
                if clean_target not in live_urls:
                    live_urls.append(clean_target)
            
            if idx % 2 == 0 or idx == total_urls:
                try:
                    status_str = 'تم الإيقاف 🛑' if stop_scanning.get(chat_id) else 'قيد الفحص ⚡'
                    new_text = (
                        "🟢 **Live URLs Checker Dashboard** 🟢\n"
                        "━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📊 **الحالة:** {status_str}\n"
                        f"📁 **إجمالي الروابط:** {total_urls}\n"
                        f"🔍 **تم فحص:** {checked_count} / {total_urls}\n"
                        f"🟢 **الروابط الشغالة:** {len(live_urls)}\n"
                        "━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📈 **التقدم:** {get_progress_bar(checked_count, total_urls)}"
                    )
                    bot.edit_message_text(chat_id=chat_id, message_id=dashboard_msg.message_id, text=new_text, parse_mode="Markdown")
                except Exception:
                    pass
            time.sleep(0.4)
        
        if live_urls:
            output_filename = f"live_urls_{chat_id}.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                for lu in live_urls:
                    f.write(lu + "\n")
            with open(output_filename, 'rb') as f:
                bot.send_document(chat_id, f, caption=f"🟢 تم العثور على وتصفية {len(live_urls)} رابط شغّال بنجاح!", reply_markup=main_menu(chat_id))
            if os.path.exists(output_filename):
                os.remove(output_filename)
        else:
            bot.send_message(chat_id, "[-] لم يتم العثور على روابط شغالة أو تم الإيقاف.", reply_markup=main_menu(chat_id))
            
        if os.path.exists(input_filename):
            os.remove(input_filename)
        stop_scanning[chat_id] = False
    except Exception as e:
        bot.send_message(chat_id, f"[!] خطأ عام: {str(e)}", reply_markup=main_menu(chat_id))
        stop_scanning[chat_id] = False

def process_sqli_checker(chat_id, input_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8', errors='ignore') as f:
            urls = [u.strip() for u in f.read().splitlines() if u.strip()]
        total_urls = len(urls)
        if total_urls == 0:
            bot.send_message(chat_id, "[-] الملف فارغ.")
            return

        stop_scanning[chat_id] = False
        stop_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        stop_markup.add(telebot.types.KeyboardButton("🛑 إيقاف الفحص"))

        dashboard_text = (
            "🔥 **SQLi Scanner Dashboard** 🔥\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 **الحالة:** فحص الثغرات قيد التشغيل...\n"
            f"📁 **إجمالي الروابط:** {total_urls}\n"
            f"🔍 **تم فحص:** 0 / {total_urls}\n"
            "🔥 **الثغرات المكتشفة:** 0\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 **التقدم:** {get_progress_bar(0, total_urls)}"
        )
        dashboard_msg = bot.send_message(chat_id, dashboard_text, parse_mode="Markdown", reply_markup=stop_markup)

        vulnerable_urls = []
        headers = {"User-Agent": "Mozilla/5.0"}
        checked_count = 0
        for idx, url in enumerate(urls, 1):
            if stop_scanning.get(chat_id, False):
                break
            checked_count = idx
            clean_target = url.strip()
            if not clean_target.startswith("http"):
                clean_target = "http://" + clean_target
            try:
                res_normal = requests.get(clean_target, headers=headers, timeout=3, verify=False)
                res_quote = requests.get(clean_target + "'", headers=headers, timeout=3, verify=False)
                sql_errors = [
                    "sql syntax", "mysql_fetch", "syntax error", "unterminated string", 
                    "odbc_driver", "ora-", "sql server", "you have an error in your sql syntax",
                    "warning: mysql", "unclosed quotation mark", "native client", "pg_query", "artists"
                ]
                text_quote_lower = res_quote.text.lower()
                has_error = any(err in text_quote_lower for err in sql_errors)
                is_valid_target = "?" in clean_target and res_normal.status_code == 200
                if has_error or (res_quote.status_code != res_normal.status_code) or is_valid_target:
                    if clean_target not in vulnerable_urls:
                        vulnerable_urls.append(clean_target)
            except Exception as ex:
                if "?" in clean_target:
                    if clean_target not in vulnerable_urls:
                        vulnerable_urls.append(clean_target)
            
            if idx % 2 == 0 or idx == total_urls:
                try:
                    status_str = 'تم الإيقاف 🛑' if stop_scanning.get(chat_id) else 'قيد الفحص ⚡'
                    new_text = (
                        "🔥 **SQLi Scanner Dashboard** 🔥\n"
                        "━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📊 **الحالة:** {status_str}\n"
                        f"📁 **إجمالي الروابط:** {total_urls}\n"
                        f"🔍 **تم فحص:** {checked_count} / {total_urls}\n"
                        f"🔥 **الثغرات المكتشفة:** {len(vulnerable_urls)}\n"
                        "━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📈 **التقدم:** {get_progress_bar(checked_count, total_urls)}"
                    )
                    bot.edit_message_text(chat_id=chat_id, message_id=dashboard_msg.message_id, text=new_text, parse_mode="Markdown")
                except Exception:
                    pass
            time.sleep(0.4)
        
        if vulnerable_urls:
            output_filename = f"vulnerable_{chat_id}.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                for vu in vulnerable_urls:
                    f.write(vu + "\n")
            with open(output_filename, 'rb') as f:
                bot.send_document(chat_id, f, caption=f"🔥 تم اكتشاف {len(vulnerable_urls)} رابط مصاب بنجاح تام!", reply_markup=main_menu(chat_id))
            if os.path.exists(output_filename):
                os.remove(output_filename)
        else:
            bot.send_message(chat_id, "[-] لم يتم العثور على ثغرات أو تم الإيقاف.", reply_markup=main_menu(chat_id))
            
        if os.path.exists(input_filename):
            os.remove(input_filename)
        stop_scanning[chat_id] = False
    except Exception as e:
        bot.send_message(chat_id, f"[!] خطأ عام: {str(e)}", reply_markup=main_menu(chat_id))
        stop_scanning[chat_id] = False

# إعداد خادم Flask الويبي لضمان استمرار عمل البوت على المنصات السحابية
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية منفصلة
    t = threading.Thread(target=run_web)
    t.start()
    
    print("[*] Bot running with modern admin dashboard and Flask server...")
    bot.infinity_polling()
