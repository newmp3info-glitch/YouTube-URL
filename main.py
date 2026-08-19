import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

# Get Token strictly from Render environment variable
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Your Render app primary URL
RENDER_URL = "https://youtube-url.onrender.com"

@app.route('/')
def home():
    return "Bot is active and running!"

# Webhook route to receive updates from Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    else:
        return "Forbidden", 403

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me any YouTube, Facebook, or Instagram video link, and I will show download options.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    if "http" in url:
        msg = bot.reply_to(message, "Fetching video info, please wait...")
        try:
            ydl_opts = {
                'noplaylist': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                markup = InlineKeyboardMarkup()
                found = False
                
                for f in formats:
                    if f.get('filesize') and f.get('height') in [360, 720, 1080]:
                        size_mb = round(f['filesize'] / (1024 * 1024), 2)
                        btn_text = f"{f['height']}p - {size_mb}MB"
                        markup.add(InlineKeyboardButton(btn_text, callback_data=f"{f['format_id']}|{url}"))
                        found = True
                
                if found:
                    bot.edit_message_text(f"Video: {info.get('title')}\nChoose quality:", 
                                          chat_id=message.chat.id, message_id=msg.message_id, reply_markup=markup)
                else:
                    bot.edit_message_text("Sorry, couldn't find proper quality options for this video.", 
                                          chat_id=message.chat.id, message_id=msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"Error: {str(e)}", chat_id=message.chat.id, message_id=msg.message_id)
    else:
        bot.reply_to(message, "Please send a valid link.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('|')
    fmt_id = data[0]
    url = data[1]
    
    bot.answer_callback_query(call.id, "Generating link...")
    
    ydl_opts = {
        'format': fmt_id,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        direct_url = info.get('url')
        bot.send_message(call.message.chat.id, f"Here is your download link:\n{direct_url}")

if __name__ == "__main__":
    # Remove old webhook and set the new one
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
