import os
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

# Get Token strictly from Render environment variable
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active and running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me any YouTube, Facebook, or Instagram video link, and I will show download options.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    if "http" in url:
        msg = bot.reply_to(message, "Fetching video info, please wait...")
        try:
            ydl_opts = {'noplaylist': True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Filter formats to show only common ones with video+audio
                markup = InlineKeyboardMarkup()
                found = False
                
                for f in formats:
                    # Filter for 360p, 720p, 1080p which have file size info
                    if f.get('filesize') and f.get('height') in [360, 720, 1080]:
                        size_mb = round(f['filesize'] / (1024 * 1024), 2)
                        btn_text = f"{f['height']}p - {size_mb}MB"
                        # Use format_id as callback_data
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
    
    with YoutubeDL({'format': fmt_id}) as ydl:
        info = ydl.extract_info(url, download=False)
        direct_url = info.get('url')
        bot.send_message(call.message.chat.id, f"Here is your download link:\n{direct_url}")

def run_bot():
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
