# test_render_db.py
import os
import psycopg2
from sqlalchemy import create_engine, text

def test_render_connection():
    print("🧪 Testing Render Database Connection...")
    
    # Thông tin database từ Render
    DB_HOST = "dpg-d37h9sggjchc73c9qe5g-a.singapore-postgres.render.com"
    DB_PORT = "5432"
    DB_NAME = "telegram_rss_bot"
    DB_USER = "bot_user"
    DB_PASS = "WI7nSuSYrbD9PV2oh2zwJbO8vVnXKexg"
    
    # Cách 1: Dùng psycopg2 (low-level)
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            sslmode="require"  # Render yêu cầu SSL
        )
        print("✅ psycopg2 connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ psycopg2 error: {e}")
    
    # Cách 2: Dùng SQLAlchemy (như trong app)
    try:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ SQLAlchemy connection successful!")
            print(f"📊 PostgreSQL version: {version}")
            
    except Exception as e:
        print(f"❌ SQLAlchemy error: {e}")

if __name__ == "__main__":
    test_render_connection()