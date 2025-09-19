from datetime import datetime, timedelta
from database.json_manager import load_posted, load_ads, load_sources, load_channels
from utils.logger import logger

class StatsService:
    def get_daily_stats(self):
        """Lấy thống kê theo ngày"""
        posted = load_posted()
        ads = load_ads()
        
        today = datetime.now().date()
        daily_posts = 0
        daily_ads = 0
        
        for post in posted.values():
            post_date = datetime.fromisoformat(post['posted_at']).date()
            if post_date == today:
                daily_posts += 1
        
        for ad in ads.values():
            daily_ads += ad['times_posted']
        
        return {
            'daily_posts': daily_posts,
            'daily_ads': daily_ads,
            'total_posts': len(posted),
            'total_ads': sum(ad['times_posted'] for ad in ads.values())
        }
    
    def get_source_stats(self):
        """Thống kê theo nguồn"""
        posted = load_posted()
        source_stats = {}
        
        for post in posted.values():
            source = post['source']
            if source not in source_stats:
                source_stats[source] = 0
            source_stats[source] += 1
        
        return source_stats
    
    def get_channel_stats(self):
        """Thống kê theo kênh"""
        posted = load_posted()
        channel_stats = {}
        
        for post in posted.values():
            channel = post['channel']
            if channel not in channel_stats:
                channel_stats[channel] = 0
            channel_stats[channel] += 1
        
        return channel_stats
    
    def get_weekly_stats(self):
        """Thống kê theo tuần"""
        posted = load_posted()
        weekly_stats = {}
        
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).date()
            weekly_stats[date.strftime("%Y-%m-%d")] = 0
        
        for post in posted.values():
            post_date = datetime.fromisoformat(post['posted_at']).date()
            date_str = post_date.strftime("%Y-%m-%d")
            if date_str in weekly_stats:
                weekly_stats[date_str] += 1
        
        return weekly_stats

# Khởi tạo service
stats_service = StatsService()