# services/telegram_service.py
import requests
from config import BOT_TOKEN
from utils.logger import logger

def send_to_channel(channel_id, message, image_path=None):
    """Gửi bài viết đến kênh Telegram với xử lý lỗi chi tiết"""
    try:
        if image_path:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            with open(image_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': channel_id, 'caption': message}
                response = requests.post(url, files=files, data=data)
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {'chat_id': channel_id, 'text': message}
            response = requests.post(url, data=data)
        
        result = response.json()
        
        if response.status_code == 200:
            return True
        else:
            logger.error(f"❌ Lỗi gửi đến {channel_id}: {result.get('description', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Exception khi gửi đến {channel_id}: {e}")
        return False