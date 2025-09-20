# handlers/message_handlers.py
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import user_state
from database.json_manager import load_channels, save_channels
from handlers.menu_handlers import manage_channels, main_menu
from services.ad_service import ad_service

def handle_message(update: Update, context: CallbackContext):
    """Xử lý tin nhắn văn bản"""
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    chat_id = update.message.chat_id

    print(f"User {user_id} state: {user_state.get(user_id)}")
    print(f"Message: {text}")

    try:
        if user_state.get(user_id) == "adding_channel":
            # Xử lý thêm kênh
            channels = load_channels()
            
            # Kiểm tra định dạng kênh
            if not (text.startswith('@') or text.startswith('-100')):
                update.message.reply_text(
                    "⚠️ Định dạng không đúng! Vui lòng sử dụng @username hoặc -1001234567890",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Quay lại", callback_data="manage_channels")]
                    ])
                )
                return
            
            # Thêm kênh mới
            channels[text] = {
                "title": text,
                "username": text.lstrip("@"),
                "added_date": str(datetime.now())
            }
            save_channels(channels)

            # Xóa trạng thái
            user_state[user_id] = None
            
            # Gửi thông báo thành công
            update.message.reply_text(f"✅ Đã thêm kênh {text}")
            
            # Quay lại menu quản lý kênh
            manage_channels(update, context)
            
        elif user_state.get(user_id) == "creating_ad":
            # Xử lý tạo quảng cáo mới
            if "|" not in text:
                update.message.reply_text("⚠️ Vui lòng sử dụng định dạng: Tiêu đề|Nội dung")
                return
                
            title, content = text.split("|", 1)
            
            ad_id = ad_service.create_ad(title.strip(), content.strip())
            
            user_state[user_id] = None
            
            update.message.reply_text(
                f"✅ Đã tạo quảng cáo thành công!\n\nTiêu đề: {title.strip()}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📢 Quản lý quảng cáo", callback_data="manage_ads")],
                    [InlineKeyboardButton("🔙 Menu chính", callback_data="back_main")]
                ])
            )
            
        else:
            # Nếu không có trạng thái, hiển thị menu chính
            main_menu(update, context)
            
    except Exception as e:
        print(f"Error handling message: {e}")
        update.message.reply_text("❌ Có lỗi xảy ra! Vui lòng thử lại.")
        user_state[user_id] = None
