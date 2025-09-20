from sqlalchemy.orm import Session
from database.config import SessionLocal
from database.models import PostedArticle, Ad, Source, Channel
from datetime import datetime, timedelta

class StatsService:
    def __init__(self):
        self.db = SessionLocal()
    
    def get_daily_stats(self):
        today = datetime.now().date()
        
        daily_posts = self.db.query(PostedArticle).filter(
            PostedArticle.posted_at >= today
        ).count()
        
        daily_ads = self.db.query(Ad).filter(
            Ad.times_posted > 0
        ).count()
        
        total_posts = self.db.query(PostedArticle).count()
        total_ads = self.db.query(Ad).count()
        
        return {
            'daily_posts': daily_posts,
            'daily_ads': daily_ads,
            'total_posts': total_posts,
            'total_ads': total_ads
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