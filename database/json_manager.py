import json
from pathlib import Path
from typing import Any, Dict

def load_json(file_path: Path) -> Dict[str, Any]:
    """Đọc dữ liệu từ file JSON"""
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_json(file_path: Path, data: Dict[str, Any]) -> None:
    """Ghi dữ liệu vào file JSON"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_channels():
    """Tải danh sách kênh"""
    from config import CHANNELS_FILE
    return load_json(CHANNELS_FILE)

def save_channels(data):
    """Lưu danh sách kênh"""
    from config import CHANNELS_FILE
    save_json(CHANNELS_FILE, data)

def load_sources():
    """Tải danh sách nguồn RSS"""
    from config import SOURCES_FILE
    return load_json(SOURCES_FILE)

def save_sources(data):
    """Lưu danh sách nguồn RSS"""
    from config import SOURCES_FILE
    save_json(SOURCES_FILE, data)

def load_ads():
    """Tải danh sách quảng cáo"""
    from config import ADS_FILE
    return load_json(ADS_FILE)

def save_ads(data):
    """Lưu danh sách quảng cáo"""
    from config import ADS_FILE
    save_json(ADS_FILE, data)

def load_schedules():
    """Tải lịch đăng bài"""
    from config import SCHEDULES_FILE
    return load_json(SCHEDULES_FILE)

def save_schedules(data):
    """Lưu lịch đăng bài"""
    from config import SCHEDULES_FILE
    save_json(SCHEDULES_FILE, data)

def load_posted():
    """Tải danh sách bài viết đã đăng"""
    from config import POSTED_FILE
    return load_json(POSTED_FILE)

def save_posted(data):
    """Lưu danh sách bài viết đã đăng"""
    from config import POSTED_FILE
    save_json(POSTED_FILE, data)