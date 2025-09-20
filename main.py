import os
import sys
import asyncio
import threading
from pathlib import Path
from flask import Flask
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Thêm path tới project
sys.path.append(str(Path(__file__).parent))

# Import các phần bạn đã viết
from config import BOT_TOKEN
from handlers.command_handlers import start, articles_command, dashboard_command
from handlers.callback_handlers import button_handler
from handlers.message_handlers import handle_message
from services.auto_poster import auto_poster
from utils.error_handler import error_handler

# ================== WEB SERVER (KEEP-ALIVE) ==================
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Telegram bot is alive on Render!"

def run_web():
    """Chạy web server trên PORT mà Render yêu cầu"""
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================== TELEGRAM BOT ==================
def run_bot():
    """Khởi chạy bot Telegram"""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("articles", articles_command))
    dp.add_handler(CommandHandler("dashboard", dashboard_command))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error_handler)

    # Auto poster chạy trong thread riêng
    def start_auto_poster():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(auto_poster.start())

    auto_poster_thread = threading.Thread(target=start_auto_poster)
    auto_poster_thread.daemon = True
    auto_poster_thread.start()

    print("🤖 Bot đã chạy!")
    updater.start_polling()
    updater.idle()

# ================== MAIN ==================
if __name__ == "__main__":
    # Chạy web server trong 1 thread
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    # Chạy bot chính
    run_bot()