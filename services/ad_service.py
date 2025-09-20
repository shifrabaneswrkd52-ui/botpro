from sqlalchemy.orm import Session
from database.config import SessionLocal
from database.models import Ad
from utils.logger import logger

class AdService:
    def __init__(self):
        self.db = SessionLocal()
    
    def create_ad(self, title, content, image_path=None, schedule=None):
        try:
            ad = Ad(
                title=title,
                content=content,
                image_path=image_path,
                schedule=schedule
            )
            self.db.add(ad)
            self.db.commit()
            self.db.refresh(ad)
            return ad.id
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating ad: {e}")
            return None
    
    def get_all_ads(self):
        return self.db.query(Ad).all()
    
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