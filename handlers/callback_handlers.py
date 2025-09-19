from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from config import user_state
from handlers.menu_handlers import (
    main_menu, manage_channels, manage_articles, 
    newspaper_categories, handle_category_selection, view_sources,
    delete_channel, delete_source, view_articles,
    manage_schedules, channel_schedule_menu, show_dashboard,
    manage_ads, create_ad_menu, view_stats, view_posted_articles
)
from database.json_manager import load_channels

def button_handler(update: Update, context: CallbackContext):
    """Xử lý tất cả callback queries"""
    query = update.callback_query
    query.answer()
    data = query.data
    user_id = str(query.from_user.id)

    if data == "manage_channels":
        manage_channels(update, context)

    elif data == "manage_articles":
        manage_articles(update, context)

    elif data == "view_sources":
        view_sources(update, context)

    elif data == "view_articles":
        view_articles(update, context)

    elif data == "manage_schedules":
        manage_schedules(update, context)

    elif data == "manage_ads":
        manage_ads(update, context)

    elif data == "dashboard":
        show_dashboard(update, context)

    elif data == "view_stats":
        view_stats(update, context)

    elif data == "view_posted_articles":
        view_posted_articles(update, context)

    elif data.startswith("newspaper_"):
        newspaper_name = data.replace("newspaper_", "")
        newspaper_categories(update, context, newspaper_name)

    elif data.startswith("category_"):
        parts = data.replace("category_", "").split("_", 1)
        if len(parts) >= 2:
            newspaper_name = parts[0]
            category_name = parts[1]
            handle_category_selection(update, context, newspaper_name, category_name)
        else:
            query.edit_message_text("⚠️ Lỗi: Không xác định được chuyên mục.")

    elif data == "add_channel":
        query.edit_message_text("👉 Gửi @username hoặc ID kênh mà bạn muốn thêm.")
        user_state[user_id] = "adding_channel"

    elif data.startswith("channel_"):
        chat_id = data.replace("channel_", "")
        # Xử lý menu kênh cụ thể
        channels = load_channels()
        if chat_id in channels:
            query.edit_message_text(f"📌 Menu kênh: {channels[chat_id]['title']} ({chat_id})")
        else:
            query.edit_message_text("⚠️ Kênh không tồn tại.")

    elif data.startswith("delete_channel_"):
        channel_id = data.replace("delete_channel_", "")
        delete_channel(update, context, channel_id)

    elif data.startswith("delete_source_"):
        source_id = data.replace("delete_source_", "")
        delete_source(update, context, source_id)

    elif data.startswith("channel_schedule_"):
        channel_id = data.replace("channel_schedule_", "")
        channel_schedule_menu(update, context, channel_id)

    elif data.startswith("add_schedule_"):
        parts = data.replace("add_schedule_", "").split("_")
        if len(parts) >= 2:
            channel_id = parts[0]
            interval = int(parts[1])
            from services.schedule_service import schedule_service
            schedule_id = schedule_service.add_schedule(channel_id, interval)
            query.edit_message_text(f"✅ Đã thêm lịch đăng bài mới!")
            channel_schedule_menu(update, context, channel_id)

    elif data.startswith("delete_schedules_"):
        channel_id = data.replace("delete_schedules_", "")
        from services.schedule_service import schedule_service
        schedules = schedule_service.get_channel_schedules(channel_id)
        for schedule_id in list(schedules.keys()):
            schedule_service.delete_schedule(schedule_id)
        query.edit_message_text(f"✅ Đã xóa tất cả lịch đăng bài!")
        channel_schedule_menu(update, context, channel_id)

    elif data == "create_ad":
        create_ad_menu(update, context)

    elif data == "clear_posted_history":
        from database.json_manager import save_posted
        save_posted({})
        query.edit_message_text("✅ Đã xóa lịch sử bài đăng!")
        view_posted_articles(update, context)

    elif data == "back_main":
        main_menu(update, context)

    else:
        query.edit_message_text("⚠️ Tính năng này chưa được triển khai.", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Trở lại", callback_data="back_main")]
        ]))