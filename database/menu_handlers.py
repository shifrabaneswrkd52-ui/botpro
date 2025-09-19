from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from config import NEWSPAPERS
from database.json_manager import load_json, save_json
from services.rss_service import get_rss_feed_info

def manage_articles(update: Update, context: CallbackContext):
    """Hiển thị menu chọn báo"""
    query = update.callback_query
    query.answer()
    
    keyboard = []
    row = []
    
    newspapers = list(NEWSPAPERS.keys())
    for i, newspaper in enumerate(newspapers, 1):
        row.append(InlineKeyboardButton(f"{i}", callback_data=f"newspaper_{newspaper}"))
        if i % 4 == 0:
            keyboard.append(row)
            row = []
    
    keyboard.append([InlineKeyboardButton("🔙 Trở lại", callback_data="back_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        "📰 Chọn báo để quản lý nguồn tin:\n\n" +
        "\n".join([f"{i}. {paper}" for i, paper in enumerate(newspapers, 1)]),
        reply_markup=reply_markup
    )