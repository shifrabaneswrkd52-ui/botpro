# test_database.py
from database.config import engine
from sqlalchemy import text

def test_database():
    try:
        with engine.connect() as conn:
            # Kiểm tra channels
            result = conn.execute(text('SELECT * FROM channels'))
            channels = result.fetchall()
            print('Channels:', channels)
            
            # Kiểm tra sources  
            result = conn.execute(text('SELECT newspaper, category FROM sources'))
            sources = result.fetchall()
            print('Sources:', sources)
            
            print('✅ Database test passed!')
            
    except Exception as e:
        print(f'❌ Database error: {e}')

if __name__ == "__main__":
    test_database()
