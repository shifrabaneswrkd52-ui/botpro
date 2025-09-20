# test_channel.py
from services.telegram_service import send_to_channel

def test_channel_permissions():
    channel_id = "@tin_tuc_moi_nhat"  # Thay bằng channel của bạn
    test_message = "🤖 Test quyền bot - Nếu bạn thấy tin nhắn này, bot có quyền post!"
    
    success = send_to_channel(channel_id, test_message)
    
    if success:
        print("✅ Bot có quyền gửi tin nhắn!")
    else:
        print("❌ Bot không có quyền gửi tin nhắn!")

if __name__ == "__main__":
    test_channel_permissions()