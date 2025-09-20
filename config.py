from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


# Đường dẫn thư mục
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = BASE_DIR / "image"

# Tạo thư mục nếu chưa tồn tại
DATA_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(exist_ok=True)

# File paths
CHANNELS_FILE = DATA_DIR / "channels.json"
SOURCES_FILE = DATA_DIR / "sources.json"
ARTICLES_FILE = DATA_DIR / "articles.json"
ADS_FILE = DATA_DIR / "ads.json"
SCHEDULES_FILE = DATA_DIR / "schedules.json"
POSTED_FILE = DATA_DIR / "posted.json"
TOKEN_FILE = DATA_DIR / "telegraph_token.json"

# Bot token
BOT_TOKEN ="8344274130:AAHG5kqyHPAlwjJIIgRvjjOmFNf3yUJApgU"

# Dữ liệu các báo và RSS feeds
NEWSPAPERS = {
    "VnExpress": {
        "Thời sự": "https://vnexpress.net/rss/thoi-su.rss",
        "Thế giới": "https://vnexpress.net/rss/the-gioi.rss",
        "Kinh doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
        "Giải trí": "https://vnexpress.net/rss/giai-tri.rss",
        "Thể thao": "https://vnexpress.net/rss/the-thao.rss",
        "Du lịch": "https://vnexpress.net/rss/du-lich.rss",
        "Khoa học": "https://vnexpress.net/rss/khoa-hoc.rss",
        "Sức khỏe": "https://vnexpress.net/rss/suc-khoe.rss",
        "Pháp luật": "https://vnexpress.net/rss/phap-luat.rss",
        "Giáo dục": "https://vnexpress.net/rss/giao-duc.rss",
        "Xe": "https://vnexpress.net/rss/xe.rss",
        "Công nghệ": "https://vnexpress.net/rss/cong-nghe.rss",
        "Đời sống": "https://vnexpress.net/rss/doi-song.rss",
        "Video": "https://vnexpress.net/rss/video.rss"
    },
    "Dân Trí": {
        "Thời sự": "https://dantri.com.vn/rss/thoi-su.rss",
        "Giáo dục": "https://dantri.com.vn/rss/giao-duc.rss",
        "Sức khỏe": "https://dantri.com.vn/rss/suc-khoe.rss",
        "Kinh doanh": "https://dantri.com.vn/rss/kinh-doanh.rss",
        "Đời sống": "https://dantri.com.vn/rss/doi-song.rss",
        "Thế giới": "https://dantri.com.vn/rss/the-gioi.rss",
        "Du lịch": "https://dantri.com.vn/rss/du-lich.rss",
        "Xe": "https://dantri.com.vn/rss/xe.rss",
        "Nhân ái": "https://dantri.com.vn/rss/nhan-ai.rss",
        "Công sở": "https://dantri.com.vn/rss/cong-so.rss",
        "Nhịp sống trẻ": "https://dantri.com.vn/rss/nhip-song-tre.rss"
    },
    "VietnamNet": {
        "Chính trị": "https://vietnamnet.vn/rss/chinh-tri.rss",
        "Thời sự": "https://vietnamnet.vn/rss/thoi-su.rss",
        "Kinh doanh": "https://vietnamnet.vn/rss/kinh-doanh.rss",
        "Thế giới": "https://vietnamnet.vn/rss/the-gioi.rss",
        "Giáo dục": "https://vietnamnet.vn/rss/giao-duc.rss",
        "Đời sống": "https://vietnamnet.vn/rss/doi-song.rss",
        "Văn hóa - Giải trí": "https://vietnamnet.vn/rss/van-hoa-giai-tri.rss",
        "Sức khỏe": "https://vietnamnet.vn/rss/suc-khoe.rss",
        "Công nghệ": "https://vietnamnet.vn/rss/cong-nghe.rss",
        "Pháp luật": "https://vietnamnet.vn/rss/phap-luat.rss",
        "Xe": "https://vietnamnet.vn/rss/xe.rss",
        "Bất động sản": "https://vietnamnet.vn/rss/bat-dong-san.rss",
        "Du lịch": "https://vietnamnet.vn/rss/du-lich.rss",
        "Bạn đọc": "https://vietnamnet.vn/rss/ban-doc.rss"
    },
    "Tuổi Trẻ": {
        "Thời sự": "https://tuoitre.vn/rss/thoi-su.rss",
        "Thế giới": "https://tuoitre.vn/rss/the-gioi.rss",
        "Giáo dục": "https://tuoitre.vn/rss/giao-duc.rss",
        "Sức khỏe": "https://tuoitre.vn/rss/suc-khoe.rss",
        "Giới trẻ": "https://tuoitre.vn/rss/gioi-tre.rss",
        "Văn hóa": "https://tuoitre.vn/rss/van-hoa.rss",
        "Giải trí": "https://tuoitre.vn/rss/giai-tri.rss",
        "Thể thao": "https://tuoitre.vn/rss/the-thao.rss",
        "Công nghệ": "https://tuoitre.vn/rss/cong-nghe.rss",
        "Du lịch": "https://tuoitre.vn/rss/du-lich.rss"
    },
    "Thanh Niên": {
        "Chính trị": "https://thanhnien.vn/rss/chinh-tri.rss",
        "Thời sự": "https://thanhnien.vn/rss/thoi-su.rss",
        "Thế giới": "https://thanhnien.vn/rss/the-gioi.rss",
        "Kinh tế": "https://thanhnien.vn/rss/kinh-te.rss",
        "Giáo dục": "https://thanhnien.vn/rss/giao-duc.rss",
        "Đời sống": "https://thanhnien.vn/rss/doi-song.rss",
        "Văn hóa": "https://thanhnien.vn/rss/van-hoa.rss",
        "Giải trí": "https://thanhnien.vn/rss/giai-tri.rss",
        "Thể thao": "https://thanhnien.vn/rss/the-thao.rss",
        "Công nghệ": "https://thanhnien.vn/rss/cong-nghe.rss",
        "Du lịch": "https://thanhnien.vn/rss/du-lich.rss"
    },
    "Zing News": {
        "Tin mới": "https://news.zing.vn/rss/tin-moi.rss",
        "Thời sự": "https://news.zing.vn/rss/thoi-su.rss",
        "Thế giới": "https://news.zing.vn/rss/the-gioi.rss",
        "Kinh doanh": "https://news.zing.vn/rss/kinh-doanh-tai-chinh.rss",
        "Pháp luật": "https://news.zing.vn/rss/phap-luat.rss",
        "Xuất bản": "https://news.zing.vn/rss/xuat-ban.rss",
        "Thể thao": "https://news.zing.vn/rss/the-thao.rss",
        "Công nghệ": "https://news.zing.vn/rss/cong-nghe.rss",
        "Ô tô – Xe máy": "https://news.zing.vn/rss/oto-xe-may.rss"
    },
    "Báo Mới": {
        "Thời sự": "https://baomoi.com/rss/thoi-su.rss",
        "Thế giới": "https://baomoi.com/rss/the-gioi.rss",
        "Kinh doanh": "https://baomoi.com/rss/kinh-doanh.rss",
        "Giải trí": "https://baomoi.com/rss/giai-tri.rss",
        "Thể thao": "https://baomoi.com/rss/the-thao.rss",
        "Công nghệ": "https://baomoi.com/rss/cong-nghe.rss",
        "Sức khỏe": "https://baomoi.com/rss/suc-khoe.rss",
        "Đời sống": "https://baomoi.com/rss/doi-song.rss"
    },
    "Vietnam News": {
        "Politics": "https://vnanet.vn/en/rss/politics.rss",
        "Society": "https://vnanet.vn/en/rss/society.rss",
        "Economy": "https://vnanet.vn/en/rss/economy.rss",
        "Culture": "https://vnanet.vn/en/rss/culture.rss",
        "Sports": "https://vnanet.vn/en/rss/sports.rss",
        "Science & Tech": "https://vnanet.vn/en/rss/science-technology.rss",
        "Health": "https://vnanet.vn/en/rss/health.rss",
        "Environment": "https://vnanet.vn/en/rss/environment.rss",
        "Education": "https://vnanet.vn/en/rss/education.rss",
        "World": "https://vnanet.vn/en/rss/world.rss"
    }
}

SCHEDULE_OPTIONS = {
    "5_minutes": 300,
    "15_minutes": 900,
    "30_minutes": 1800,
    "1_hour": 3600,
    "3_hours": 10800,
    "6_hours": 21600,
    "12_hours": 43200,
    "1_day": 86400
}

# State management
user_state = {}
