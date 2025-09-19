import requests
from config import BOT_TOKEN
from utils.logger import logger

def send_to_channel(channel_id, message, image_path=None):
    """Gửi bài viết đến kênh Telegram (phiên bản sync)"""
    if image_path:
        # Gửi ảnh
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': channel_id, 'caption': message}
            response = requests.post(url, files=files, data=data)
    else:
        # Gửi tin nhắn văn bản
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {'chat_id': channel_id, 'text': message}
        response = requests.post(url, data=data)
    
    return response.status_code == 200