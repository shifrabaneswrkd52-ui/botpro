from typing import Any, Dict
import re

def is_valid_url(url: str) -> bool:
    """Kiểm tra URL có hợp lệ không"""
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

def truncate_text(text: str, max_length: int = 100) -> str:
    """Cắt ngắn văn bản nếu quá dài"""
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text

def safe_get(dictionary: Dict[Any, Any], keys: List[Any], default: Any = None) -> Any:
    """Lấy giá trị từ dictionary một cách an toàn"""
    current = dictionary
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current