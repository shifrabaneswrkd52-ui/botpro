import sys
import json
from datetime import datetime
from pathlib import Path

# Thêm đường dẫn đến thư mục gốc
sys.path.append(str(Path(__file__).parent.parent))

from database.config import SessionLocal
from database.models import Channel, Source, Ad, Schedule

def migrate_json_to_db():
    """Chuyển dữ liệu từ JSON files sang database"""
    db = SessionLocal()
    
    try:
        # Migration channels
        channels_file = Path("data/channels.json")
        if channels_file.exists() and channels_file.stat().st_size > 0:
            with open(channels_file, "r", encoding="utf-8") as f:
                channels_data = json.load(f)
            
            for channel_id, channel_info in channels_data.items():
                channel = Channel(
                    channel_id=channel_id,
                    title=channel_info.get('title', ''),
                    username=channel_info.get('username', ''),
                    added_date=datetime.fromisoformat(channel_info.get('added_date', str(datetime.now())))
                )
                db.add(channel)
            print(f"✅ Đã migration {len(channels_data)} channels")
        
        # Migration sources
        sources_file = Path("data/sources.json")
        if sources_file.exists() and sources_file.stat().st_size > 0:
            with open(sources_file, "r", encoding="utf-8") as f:
                sources_data = json.load(f)
            
            for source_id, source_info in sources_data.items():
                source = Source(
                    newspaper=source_info.get('newspaper', ''),
                    category=source_info.get('category', ''),
                    rss_url=source_info.get('rss_url', ''),
                    title=source_info.get('title', ''),
                    description=source_info.get('description', ''),
                    link=source_info.get('link', ''),
                    added_date=datetime.fromisoformat(source_info.get('added_date', str(datetime.now())))
                )
                db.add(source)
            print(f"✅ Đã migration {len(sources_data)} sources")
        
        # Migration ads
        ads_file = Path("data/ads.json")
        if ads_file.exists() and ads_file.stat().st_size > 0:
            with open(ads_file, "r", encoding="utf-8") as f:
                ads_data = json.load(f)
            
            for ad_id, ad_info in ads_data.items():
                ad = Ad(
                    title=ad_info.get('title', ''),
                    content=ad_info.get('content', ''),
                    image_path=ad_info.get('image_path'),
                    schedule=ad_info.get('schedule'),
                    created_at=datetime.fromisoformat(ad_info.get('created_at', str(datetime.now()))),
                    is_active=ad_info.get('is_active', True),
                    times_posted=ad_info.get('times_posted', 0)
                )
                db.add(ad)
            print(f"✅ Đã migration {len(ads_data)} ads")
        else:
            print("ℹ️ File ads.json trống hoặc không tồn tại, bỏ qua")
        
        db.commit()
        print("🎉 Migration dữ liệu hoàn tất!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi migration: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_json_to_db()