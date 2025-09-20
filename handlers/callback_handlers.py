# handlers/callback_handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import user_state
from handlers.menu_handlers import (
    main_menu, manage_channels, manage_articles, 
    newspaper_categories, handle_category_selection, view_sources,
    delete_channel, delete_source, view_articles,
    manage_schedules, channel_schedule_menu, show_dashboard,
    manage_ads, create_ad_menu, view_stats, view_posted_articles,
    manage_backup, channel_detail_menu
)
from database.json_manager import load_channels
from services.schedule_service import schedule_service
from services.ad_service import ad_service
from services.backup_service import backup_service
from services.stats_service import stats_service

def button_handler(update: Update, context: CallbackContext):
    """Xử lý tất cả callback queries"""
    query = update.callback_query
    query.answer()
    data = query.data
    user_id = str(query.from_user.id)

    # Debug: in callback data
    print(f"Callback data: {data}")

    try:
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

        elif data == "manage_backup":
            manage_backup(update, context)

        elif data == "create_ad":
            create_ad_menu(update, context)
            user_state[user_id] = "creating_ad"

        elif data == "back_main":
            main_menu(update, context)

        elif data.startswith("newspaper_"):
            newspaper_name = data.replace("newspaper_", "")
            newspaper_categories(update, context, newspaper_name)

        elif data.startswith("category_"):
            parts = data.replace("category_", "").split("_", 1)
            if len(parts) >= 2:
                newspaper_name = parts[0]
                category_name = parts[1]
                handle_category_selection(update, context, newspaper_name, category_name)

        elif data.startswith("channel_"):
            channel_id = data.replace("channel_", "")
            channel_detail_menu(update, context, channel_id)

        elif data.startswith("channel_schedule_"):
            channel_id = data.replace("channel_schedule_", "")
            channel_schedule_menu(update, context, channel_id)

        elif data.startswith("add_schedule_"):
            parts = data.replace("add_schedule_", "").split("_")
            if len(parts) >= 2:
                channel_id = parts[0]
                interval = int(parts[1])
                schedule_id = schedule_service.add_schedule(channel_id, interval)
                query.edit_message_text(f"✅ Đã thêm lịch đăng bài mới!")
                channel_schedule_menu(update, context, channel_id)

        elif data.startswith("delete_schedules_"):
            channel_id = data.replace("delete_schedules_", "")
            schedules = schedule_service.get_channel_schedules(channel_id)
            for schedule_id in list(schedules.keys()):
                schedule_service.delete_schedule(schedule_id)
            query.edit_message_text(f"✅ Đã xóa tất cả lịch đăng bài!")
            channel_schedule_menu(update, context, channel_id)

        elif data == "create_backup":
            backup_path = backup_service.create_backup()
            query.edit_message_text(f"✅ Đã tạo backup thành công!")
            manage_backup(update, context)

        elif data == "clear_posted_history":
            from database.json_manager import save_posted
            save_posted({})
            query.edit_message_text("✅ Đã xóa lịch sử bài đăng!")
            view_posted_articles(update, context)

        elif data == "list_ads":
            from handlers.menu_handlers import list_ads
            list_ads(update, context)

        elif data.startswith("delete_channel_"):
            channel_id = data.replace("delete_channel_", "")
            from handlers.menu_handlers import delete_channel
            delete_channel(update, context, channel_id)

        elif data.startswith("delete_source_"):
            source_id = data.replace("delete_source_", "")
            from handlers.menu_handlers import delete_source
            delete_source(update, context, source_id)

        elif data == "check_updates":
            from services.update_service import update_service
            update_info = update_service.check_for_updates()
            if update_info['has_update']:
                message = f"🆕 Có bản cập nhật mới!\n\nPhiên bản: {update_info['version']}\n\n{update_info['release_notes']}"
            else:
                message = "✅ Bạn đang sử dụng phiên bản mới nhất!"
            query.edit_message_text(message)

        elif data == "restore_backup_menu":
            from handlers.menu_handlers import restore_backup_menu
            restore_backup_menu(update, context)

        elif data.startswith("restore_"):
            backup_name = data.replace("restore_", "")
            success = backup_service.restore_backup(backup_name)
            if success:
                query.edit_message_text("✅ Đã khôi phục backup thành công!")
            else:
                query.edit_message_text("❌ Không thể khôi phục backup!")
            manage_backup(update, context)

        else:
            query.edit_message_text(
                "⚠️ Tính năng này chưa được triển khai.", 
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Trở lại", callback_data="back_main")]
                ])
            )

    except Exception as e:
        print(f"Error in button handler: {e}")
        query.edit_message_text(
            "❌ Đã xảy ra lỗi! Vui lòng thử lại.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
            ])
        )
