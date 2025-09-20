import sys
import os
from pathlib import Path

# Thêm đường dẫn đến thư mục gốc
sys.path.append(str(Path(__file__).parent.parent))

from database.config import engine, Base
from database.models import Channel, Source, Article, Ad, Schedule, PostedArticle
from sqlalchemy import text

def migrate_data():
    try:
        # Tạo tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Kiểm tra tables đã được tạo (SỬA LẠI)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print(f"📊 Tables created: {tables}")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    migrate_data()