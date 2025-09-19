import re

def is_valid_channel_username(username):
    """Kiểm tra username kênh có hợp lệ không"""
    pattern = r'^@[a-zA-Z0-9_]{5,32}$'
    return re.match(pattern, username) is not None

def is_valid_url(url):
    """Kiểm tra URL có hợp lệ không"""
    pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None

def is_valid_rss_url(url):
    """Kiểm tra URL RSS có hợp lệ không"""
    return is_valid_url(url) and any(ext in url for ext in ['.rss', '.xml', 'feed'])
