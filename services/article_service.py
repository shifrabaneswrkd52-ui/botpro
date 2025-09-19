import asyncio
from telegram import Bot
from config import BOT_TOKEN
from database.json_manager import load_sources
from services.rss_service import get_latest_articles
from utils.logger import logger

def get_articles_from_sources(limit=5):
    """Lấy bài viết từ tất cả nguồn"""
    sources = load_sources()
    all_articles = []
    
    for source_id, source_info in sources.items():
        articles = get_latest_articles(source_info['rss_url'], limit)
        for article in articles:
            article['source'] = source_info['newspaper']
            article['category'] = source_info['category']
            all_articles.append(article)
    
    # Sắp xếp theo thời gian (nếu có)
    all_articles.sort(key=lambda x: x.get('published', ''), reverse=True)
    return all_articles[:limit]

async def send_article_preview(chat_id, article):
    """Gửi xem trước bài viết"""
    bot = Bot(token=BOT_TOKEN)
    
    message = f"📰 {article['title']}\n\n"
    message += f"📅 {article.get('published', 'Không có ngày')}\n"
    message += f"🔗 {article['link']}\n\n"
    message += f"{article.get('summary', '')[:200]}..."
    
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logger.info(f"Lỗi khi gửi xem trước bài viết: {e}")