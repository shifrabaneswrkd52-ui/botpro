import requests
import json
from utils.logger import logger

class UpdateService:
    def __init__(self):
        self.update_url = "https://api.github.com/repos/username/telegram-rss-bot/releases/latest"
    
    def check_for_updates(self):
        """Kiểm tra cập nhật mới"""
        try:
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                latest_release = response.json()
                return {
                    'has_update': True,
                    'version': latest_release['tag_name'],
                    'release_notes': latest_release['body'],
                    'download_url': latest_release['html_url']
                }
        except Exception as e:
            logger.error(f"Lỗi khi kiểm tra cập nhật: {e}")
        
        return {'has_update': False}
    
    def get_current_version(self):
        """Lấy phiên bản hiện tại"""
        try:
            with open('version.json', 'r') as f:
                return json.load(f).get('version', '1.0.0')
        except:
            return '1.0.0'

# Khởi tạo service
update_service = UpdateService()