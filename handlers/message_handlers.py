from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from config import user_state
from database.json_manager import load_channels, save_channels
from handlers.menu_handlers import manage_channels

def handle_message(update: Update, context: CallbackContext):
    """Xử lý tin nhắn văn bản"""
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()

    if user_state.get(user_id) == "adding_channel":
        channels = load_channels()
        channels[text] = {"title": text, "username": text.lstrip("@")}
        save_channels(channels)
        update.message.reply_text(f"✅ Đã thêm kênh {text}")
        user_state[user_id] = None
        manage_channels(update, context)
        return

    elif user_state.get(user_id) == "creating_ad":
        # Xử lý tạo quảng cáo
        if "|" in text:
            title, content = text.split("|", 1)
            from services.ad_service import ad_service
            ad_id = ad_service.create_ad(title.strip(), content.strip())
            
            update.message.reply_text(
                f"✅ Đã tạo quảng cáo thành công!\n\n"
                f"📌 Tiêu đề: {title.strip()}\n"
                f"📝 Nội dung: {content.strip()[:100]}...",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📢 Quản lý quảng cáo", callback_data="manage_ads")],
                    [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
                ])
            )
            user_state[user_id] = None
        else:
            update.message.reply_text(
                "⚠️ Định dạng không đúng. Vui lòng sử dụng: Tiêu đề|Nội dung",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Quay lại", callback_data="manage_ads")]
                ])
            )
        return

    else:
        update.message.reply_text("⚠️ Vui lòng chọn thao tác từ menu.")
        from handlers.menu_handlers import main_menu
        main_menu(update, context)