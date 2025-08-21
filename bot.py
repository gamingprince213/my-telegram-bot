from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import inspect
import random

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable নেই!")

# ========================
# এখানে সব command function লিখুন
# ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমি Auto Handler Bot 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = [func for func in dir() if func.startswith("cmd_")]
    cmds_list = "\n".join(f"/{c[4:]}" for c in commands)
    await update.message.reply_text(f"Available commands:\n{cmds_list}")

# উদাহরণ নতুন command
async def cmd_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    await update.message.reply_text(text if text else "কিছু লিখুন /echo এর পরে")

async def cmd_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "কেন কম্পিউটার গরম হয়ে যায়? কারণ তার fans আছে! 😄",
        "কীভাবে প্রোগ্রামার বন্ধুদের হাসায়? debug করে! 😎",
        "Python প্রোগ্রামার সবসময় chilled থাকে। 🐍"
    ]
    await update.message.reply_text(random.choice(jokes))

# ========================
# Auto handler function
# ========================

def get_application():
    app = Application.builder().token(TOKEN).build()

    # Auto detect functions starting with 'cmd_'
    current_module = globals()
    for name, func in current_module.items():
        if callable(func) and name.startswith("cmd_"):
            command_name = name[4:]  # Remove 'cmd_' prefix
            app.add_handler(CommandHandler(command_name, func))
    
    # Add help separately
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    return app
