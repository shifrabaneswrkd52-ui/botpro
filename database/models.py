from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

@dataclass
class Channel:
    id: str
    title: str
    username: str

@dataclass
class RSSSource:
    newspaper: str
    category: str
    rss_url: str
    title: str
    description: str
    link: str
    added_date: datetime

@dataclass
class Article:
    id: str
    title: str
    content: str
    image: str
    source: str
    published_date: datetime