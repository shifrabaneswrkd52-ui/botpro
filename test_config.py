# test_config.py
def test_config():
    try:
        from config import BOT_TOKEN, BASE_DIR
        print(f"✅ Config loaded! BOT_TOKEN: {BOT_TOKEN[:10]}...")
        print(f"✅ BASE_DIR: {BASE_DIR}")
    except Exception as e:
        print(f"❌ Config error: {e}")

if __name__ == "__main__":
    test_config()
