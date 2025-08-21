from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import os
import random

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable নেই!")

# ========================
# Command Functions
# ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Echo", callback_data="echo")],
        [InlineKeyboardButton("Joke", callback_data="joke")],
        [InlineKeyboardButton("Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("হ্যালো! Command menu থেকে select করুন 👇", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start\n/help\n/echo\n/joke")

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
# Callback Handler for Keyboard
# ========================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "echo":
        await query.edit_message_text("Type /echo followed by your message")
    elif data == "joke":
        jokes = [
            "কেন কম্পিউটার গরম হয়ে যায়? কারণ তার fans আছে! 😄",
            "কীভাবে প্রোগ্রামার বন্ধুদের হাসায়? debug করে! 😎",
            "Python প্রোগ্রামার সবসময় chilled থাকে। 🐍"
        ]
        await query.edit_message_text(random.choice(jokes))
    elif data == "help":
        await query.edit_message_text("Commands:\n/start\n/help\n/echo\n/joke")

# ========================
# Auto Handler
# ========================

def get_application():
    from inspect import getmembers, iscoroutinefunction
    app = Application.builder().token(TOKEN).build()

    # Auto detect functions starting with 'cmd_'
    current_module = globals()
    for name, func in current_module.items():
        if iscoroutinefunction(func) and name.startswith("cmd_"):
            command_name = name[4:]
            app.add_handler(CommandHandler(command_name, func))

    # Start & Help
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # CallbackQuery for inline keyboard
    app.add_handler(CallbackQueryHandler(button))

    return app
