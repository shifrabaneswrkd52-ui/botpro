from telegram import Update
from telegram.ext import CallbackContext
from utils.logger import logger

def error_handler(update: Update, context: CallbackContext):
    try:
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            update.effective_message.reply_text(
                "❌ Đã xảy ra lỗi! Vui lòng thử lại sau."
            )
    except Exception as e:
        logger.error(f"Error in error handler: {e}")