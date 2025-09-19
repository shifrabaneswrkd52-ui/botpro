import os
import sys
import asyncio
from services.auto_poster import auto_poster
from pathlib import Path
from handlers.command_handlers import start, articles_command, dashboard_command

sys.path.append(str(Path(__file__).parent))

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from config import BOT_TOKEN
from handlers.command_handlers import start
from handlers.callback_handlers import button_handler
from handlers.message_handlers import handle_message
from handlers.command_handlers import start, articles_command

import asyncio
from services.auto_poster import auto_poster

def main():
    """Khởi chạy bot Telegram"""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Thêm handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("articles", articles_command))
    dp.add_handler(CommandHandler("dashboard", dashboard_command))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Bắt đầu auto-poster trong một thread riêng
    def start_auto_poster():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(auto_poster.start())
    
    import threading
    auto_poster_thread = threading.Thread(target=start_auto_poster)
    auto_poster_thread.daemon = True
    auto_poster_thread.start()

    print("🤖 Bot đã chạy!")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
