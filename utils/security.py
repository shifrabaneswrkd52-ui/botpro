import hashlib
import os
from config import BOT_TOKEN

def generate_api_key():
    """Tạo API key duy nhất"""
    return hashlib.sha256(os.urandom(32)).hexdigest()

def verify_user_access(user_id):
    """Xác minh quyền truy cập của user"""
    # Thêm logic xác minh user tại đây
    # Có thể lưu danh sách admin trong config
    return True  # Tạm thời cho phép tất cả

def sanitize_input(text):
    """Làm sạch input người dùng"""
    if not text:
        return ""
    
    # Loại bỏ các ký tự nguy hiểm
    dangerous_chars = ['<', '>', 'script', 'javascript', 'onload']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()