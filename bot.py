import telebot
from telebot import types
import os
import logging

# =========================
# إعدادات أساسية
# =========================

TOKEN = os.getenv("BOT_TOKEN")  # لازم تضيفه في Render
CHANNEL_USERNAME = "@FLASHUSDT000000"  # غيره ليوزر قناتك
STORE_LINK = "https://flashusdt00000000000.netlify.app/"  # رابط متجرك

if not TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

bot = telebot.TeleBot(TOKEN)

logging.basicConfig(level=logging.INFO)

# =========================
# التحقق من الاشتراك
# =========================

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Subscription check error: {e}")
        return False

# =========================
# أمر /start
# =========================

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if check_subscription(user_id):
        send_store(message.chat.id)
    else:
        send_subscription_message(message.chat.id)

# =========================
# رسالة الاشتراك
# =========================

def send_subscription_message(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📢 اشترك بالقناة",
            url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
        ),
        types.InlineKeyboardButton(
            "✅ تحقق من الاشتراك",
            callback_data="check_sub"
        )
    )

    bot.send_message(
        chat_id,
        "🚨 لازم تشترك بالقناة أولاً حتى تقدر تستخدم البوت 👇",
        reply_markup=markup
    )

# =========================
# إرسال المتجر
# =========================

def send_store(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = types.WebAppInfo(STORE_LINK)
    button = types.KeyboardButton("🛒 Store", web_app=web_app)
    markup.add(button)

    bot.send_message(
        chat_id,
        "✅ تم التحقق من الاشتراك\n\nأهلاً بك في المتجر 👌",
        reply_markup=markup
    )

# =========================
# زر التحقق
# =========================

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "تم التحقق ✅")
        send_store(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "لسا ما اشتركت ❌", show_alert=True)

# =========================
# تشغيل البوت
# =========================

print("Bot is running...")
bot.infinity_polling(skip_pending=True)