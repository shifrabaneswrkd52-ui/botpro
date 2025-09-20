# reset_webhook.py
from telegram import Bot
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
bot.delete_webhook()
print("✅ Webhook đã được xóa cho token mới!")