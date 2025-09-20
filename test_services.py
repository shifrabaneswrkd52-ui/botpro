# test_services.py
from services.ad_service import ad_service
from services.schedule_service import schedule_service

def test_services():
    try:
        ads = ad_service.get_all_ads()
        schedules = schedule_service.get_all_schedules()
        print(f'✅ Services loaded - Ads: {len(ads)}, Schedules: {len(schedules)}')
    except Exception as e:
        print(f'❌ Services error: {e}')

if __name__ == "__main__":
    test_services()