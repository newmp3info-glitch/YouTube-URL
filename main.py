import os
import threading
from flask import Flask
import telebot
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

@app.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me any YouTube, Facebook, or Instagram video link, and I will generate the download link for you.")

@app.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    if "http" in url:
        bot.reply_to(message, "Processing your video, please wait...")
        try:
            ydl_opts = {'format': 'best', 'noplaylist': True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url')
                title = info.get('title', 'Video')
                
                if video_url:
                    bot.reply_to(message, f"Title: {title}\n\nDirect Download Link:\n{video_url}")
                else:
                    bot.reply_to(message, "Could not fetch the download link.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {str(e)}")
    else:
        bot.reply_to(message, "Please send a valid video link containing http/https.")

def run_bot():
    # Remove active webhook to fix conflict error 409
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    # Start telegram bot in a separate background thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Run Flask app for Render & UptimeRobot pinging
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
