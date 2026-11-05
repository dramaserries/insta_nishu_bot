import os
import threading
from flask import Flask
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "9259539680:AAE6j6Ta9ozPSIsVaJp7ttuA3wX3l9NE5g0" # Yahan apna token daalein

app = Flask(_name_) # Yahan name theek kar diya hai

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "instagram.com" not in url and "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Bhai, sirf Instagram ya YouTube ka link bhejo.")
        return
    
    msg = await update.message.reply_text("Video download ho rahi hai, thoda wait karein...")
    try:
        ydl_opts = {'outtmpl': 'video.mp4', 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            await update.message.reply_video(video=video)
        os.remove('video.mp4')
        await msg.delete()
    except Exception as e:
        await msg.edit_text("Sorry, video download nahi ho payi.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    application.run_polling()

if name == 'main': # Yahan bhi name theek kar diya hai
    threading.Thread(target=run_flask).start()
    main()
