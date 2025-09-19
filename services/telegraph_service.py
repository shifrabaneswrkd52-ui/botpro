import requests
import json
from pathlib import Path
from database.json_manager import load_json, save_json
from utils.logger import logger

def get_telegraph_token():
    """Lấy hoặc tạo token Telegraph"""
    tokens = load_json(Path("data/telegraph_token.json"))
    if tokens and 'access_token' in tokens:
        return tokens['access_token']
    
    # Tạo account mới nếu chưa có token
    response = requests.get('https://api.telegra.ph/createAccount?short_name=RSSBot&author_name=RSSBot')
    if response.status_code == 200:
        token = response.json()['result']['access_token']
        save_json(Path("data/telegraph_token.json"), {'access_token': token})
        return token
    return None

def create_telegraph_page(title, content, author_name="RSS Bot", author_url="https://t.me/rss_bot"):
    """Tạo trang Telegraph mới"""
    token = get_telegraph_token()
    if not token:
        return None
    
    # Định dạng content cho Telegraph
    if isinstance(content, str):
        # Chuyển đổi plain text thành format Telegraph
        paragraphs = content.split('\n')
        formatted_content = []
        for p in paragraphs:
            if p.strip():
                formatted_content.append({"tag": "p", "children": [p.strip()]})
        
        if not formatted_content:
            formatted_content = [{"tag": "p", "children": ["No content available."]}]
    else:
        formatted_content = content
    
    # Tạo trang
    response = requests.post(
        'https://api.telegra.ph/createPage',
        data={
            'access_token': token,
            'title': title[:256],  # Telegraph giới hạn 256 ký tự cho title
            'author_name': author_name[:128],
            'author_url': author_url,
            'content': json.dumps(formatted_content),
            'return_content': False
        }
    )
    
    if response.status_code == 200:
        return response.json()['result']['url']
    return None