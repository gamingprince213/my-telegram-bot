from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable নেই!")

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! আমি Render-এ হোস্ট করা Telegram Bot 🚀")

# /help কমান্ড
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠 Available commands:\n/start\n/help\n/echo <text>")

# /echo কমান্ড
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if text:
        await update.message.reply_text(f"🔁 {text}")
    else:
        await update.message.reply_text("❌ ব্যবহার: /echo কিছু লিখুন")

def get_application():
    """Telegram bot application তৈরি করে return করে"""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("echo", echo))
    return app
