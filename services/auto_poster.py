import time
import random
import asyncio  # THÊM DÒNG NÀY
from datetime import datetime
from database.json_manager import load_sources, load_channels, load_posted, save_posted
from services.rss_service import get_latest_articles
from services.telegram_service import send_to_channel
from services.schedule_service import schedule_service
from services.ad_service import ad_service
from utils.logger import logger

class AutoPoster:
    def __init__(self):
        self.is_running = False
    
    async def start(self):
        """Bắt đầu tự động đăng bài với lịch trình"""
        self.is_running = True
        while self.is_running:
            await self.check_schedules_and_post()
            await asyncio.sleep(60)  # Kiểm tra mỗi phút
    
    async def check_schedules_and_post(self):
        """Kiểm tra lịch trình và đăng bài (tối ưu hóa)"""
        try:
            schedules = schedule_service.get_all_schedules()
            current_time = datetime.now()
        
            for schedule_id, schedule in schedules.items():
                if not schedule['enabled']:
                    continue
            
                if self.should_post_now(schedule, current_time):
                    logger.info(f"⏰ Đến giờ đăng bài cho schedule {schedule_id}")
                    await self.post_to_channel(schedule['channel_id'])
                    schedule_service.update_schedule(schedule_id, last_run=str(current_time))
                
        except Exception as e:
            logger.error(f"Lỗi trong auto-poster: {e}")
    
    def should_post_now(self, schedule, current_time):
        """Kiểm tra xem có nên đăng bài ngay bây giờ không"""
        if not schedule['last_run']:
            return True
        
        last_run = datetime.fromisoformat(schedule['last_run'])
        time_diff = (current_time - last_run).total_seconds()
        return time_diff >= schedule['interval_seconds']
    
    async def post_to_channel(self, channel_id):
        """Đăng bài đến kênh cụ thể"""
        # Đăng bài viết từ RSS
        await self.post_rss_articles(channel_id)
        
        # Đăng quảng cáo (20% cơ hội)
        if random.random() < 0.2:
            await self.post_ad(channel_id)
    
    async def post_rss_articles(self, channel_id):
        """Đăng bài viết RSS"""
        sources = load_sources()
        posted = load_posted()
        
        if not sources:
            return
        
        for source_id, source_info in sources.items():
            articles = get_latest_articles(source_info['rss_url'], 3)
            
            for article in articles:
                article_id = f"{source_id}_{article['link']}"
                
                if article_id not in posted:
                    message = self.format_article_message(article, source_info)
                    success = send_to_channel(channel_id, message)
                    
                    if success:
                        posted[article_id] = {
                            'title': article['title'],
                            'source': source_info['newspaper'],
                            'category': source_info['category'],
                            'posted_at': str(datetime.now()),
                            'channel': channel_id
                        }
                        logger.info(f"✅ Đã đăng bài đến {channel_id}: {article['title']}")
                    
                    save_posted(posted)
                    time.sleep(1)  # Chờ 1 giây giữa các bài đăng
    
    async def post_ad(self, channel_id):
        """Đăng quảng cáo ngẫu nhiên"""
        ads = ad_service.get_all_ads()
        active_ads = [ad_id for ad_id, ad in ads.items() if ad['is_active']]
        
        if active_ads:
            ad_id = random.choice(active_ads)
            ad = ads[ad_id]
            message = f"📢 {ad['title']}\n\n{ad['content']}"
            
            success = send_to_channel(channel_id, message)
            if success:
                ad_service.increment_post_count(ad_id)
                logger.info(f"✅ Đã đăng quảng cáo: {ad['title']}")
    
    def format_article_message(self, article, source_info):
        """Định dạng tin nhắn bài viết"""
        message = f"📰 {article['title']}\n\n"
        message += f"📖 {article.get('summary', '')[:200]}...\n\n"
        message += f"📰 Nguồn: {source_info['newspaper']} - {source_info['category']}\n"
        message += f"🔗 Xem thêm: {article['link']}"
        
        return message
    
    def stop(self):
        """Dừng tự động đăng bài"""
        self.is_running = False

# Khởi tạo instance
auto_poster = AutoPoster()