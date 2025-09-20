import requests
from config import BOT_TOKEN

def check_bot_health():
    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
        return response.status_code == 200
    except:
        return False

if check_bot_health():
    print("✅ Bot is healthy")
else:
    print("❌ Bot is down")