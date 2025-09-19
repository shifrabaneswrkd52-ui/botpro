import json
from datetime import datetime
from database.json_manager import load_ads, save_ads
from utils.logger import logger

class AdService:
    def __init__(self):
        self.ads = load_ads()
    
    def create_ad(self, title, content, image_path=None, schedule=None):
        """Tạo quảng cáo mới"""
        ad_id = f"ad_{len(self.ads) + 1}"
        
        self.ads[ad_id] = {
            'title': title,
            'content': content,
            'image_path': image_path,
            'schedule': schedule,
            'created_at': str(datetime.now()),
            'is_active': True,
            'times_posted': 0
        }
        
        save_ads(self.ads)
        return ad_id
    
    def get_ad(self, ad_id):
        """Lấy thông tin quảng cáo"""
        return self.ads.get(ad_id)
    
    def update_ad(self, ad_id, **kwargs):
        """Cập nhật quảng cáo"""
        if ad_id in self.ads:
            self.ads[ad_id].update(kwargs)
            save_ads(self.ads)
            return True
        return False
    
    def delete_ad(self, ad_id):
        """Xóa quảng cáo"""
        if ad_id in self.ads:
            del self.ads[ad_id]
            save_ads(self.ads)
            return True
        return False
    
    def get_all_ads(self):
        """Lấy tất cả quảng cáo"""
        return self.ads
    
    def increment_post_count(self, ad_id):
        """Tăng số lần đăng quảng cáo"""
        if ad_id in self.ads:
            self.ads[ad_id]['times_posted'] += 1
            save_ads(self.ads)

# Khởi tạo service
ad_service = AdService()