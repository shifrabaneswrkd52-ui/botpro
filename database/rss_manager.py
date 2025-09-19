import feedparser
import requests
from typing import Dict, Any

def get_rss_feed_info(rss_url: str) -> Dict[str, Any]:
    """Lấy thông tin về RSS feed"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        feed = feedparser.parse(rss_url)
        
        if feed.entries:
            return {
                'title': feed.feed.get('title', 'Không có tiêu đề'),
                'description': feed.feed.get('description', ''),
                'link': feed.feed.get('link', ''),
                'entries_count': len(feed.entries),
                'is_valid': True
            }
        else:
            return {'is_valid': False, 'error': 'Không có bài viết trong RSS'}
            
    except Exception as e:
        return {'is_valid': False, 'error': str(e)}

def validate_rss_url(rss_url: str) -> bool:
    """Kiểm tra URL RSS có hợp lệ không"""
    feed_info = get_rss_feed_info(rss_url)
    return feed_info.get('is_valid', False)