import feedparser
import requests
from typing import Dict, List, Any
from utils.logger import logger

def fetch_rss_feed(rss_url: str) -> Dict[str, Any]:
    """Lấy dữ liệu từ RSS feed"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        feed = feedparser.parse(rss_url)
        
        if feed.entries:
            return {
                'title': feed.feed.get('title', ''),
                'description': feed.feed.get('description', ''),
                'link': feed.feed.get('link', ''),
                'entries': [
                    {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', ''),
                        'content': entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
                    }
                    for entry in feed.entries
                ],
                'is_valid': True
            }
        else:
            return {'is_valid': False, 'error': 'Không có bài viết trong RSS'}
            
    except Exception as e:
        return {'is_valid': False, 'error': str(e)}

def get_latest_articles(rss_url: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Lấy các bài viết mới nhất từ RSS feed"""
    feed_data = fetch_rss_feed(rss_url)
    
    if feed_data.get('is_valid'):
        return feed_data['entries'][:limit]
    
    return []