from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from handlers.menu_handlers import view_articles
from handlers.menu_handlers import show_dashboard

def start(update: Update, context: CallbackContext):
    """Xử lý lệnh /start"""
    keyboard = [
        [InlineKeyboardButton("📌 Quản lý kênh", callback_data="manage_channels")],
        [InlineKeyboardButton("📰 Quản lý nguồn tin", callback_data="manage_articles")],
        [InlineKeyboardButton("👁️ Xem bài viết", callback_data="view_articles")],
        [InlineKeyboardButton("📢 Quản lý quảng cáo", callback_data="manage_ads")],
        [InlineKeyboardButton("⏰ Quản lý lịch đăng", callback_data="manage_schedules")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("👋 Xin chào! Đây là menu chính:", reply_markup=reply_markup)

def articles_command(update: Update, context: CallbackContext):
    """Xem bài viết mới nhất"""
    view_articles(update, context)

def dashboard_command(update: Update, context: CallbackContext):
    """Hiển thị dashboard"""
    show_dashboard(update, context)