import json
from datetime import datetime, time as dt_time
from database.json_manager import load_schedules, save_schedules
from utils.logger import logger

class ScheduleService:
    def __init__(self):
        self.schedules = load_schedules()
    
    def add_schedule(self, channel_id, interval_seconds, enabled=True):
        """Thêm lịch đăng bài mới"""
        schedule_id = f"schedule_{len(self.schedules) + 1}"
        
        self.schedules[schedule_id] = {
            'channel_id': channel_id,
            'interval_seconds': interval_seconds,
            'enabled': enabled,
            'last_run': None,
            'next_run': None,
            'created_at': str(datetime.now())
        }
        
        save_schedules(self.schedules)
        return schedule_id
    
    def update_schedule(self, schedule_id, **kwargs):
        """Cập nhật lịch đăng bài"""
        if schedule_id in self.schedules:
            self.schedules[schedule_id].update(kwargs)
            save_schedules(self.schedules)
            return True
        return False
    
    def delete_schedule(self, schedule_id):
        """Xóa lịch đăng bài"""
        if schedule_id in self.schedules:
            del self.schedules[schedule_id]
            save_schedules(self.schedules)
            return True
        return False
    
    def get_channel_schedules(self, channel_id):
        """Lấy lịch đăng bài của kênh"""
        return {k: v for k, v in self.schedules.items() if v['channel_id'] == channel_id}
    
    def get_all_schedules(self):
        """Lấy tất cả lịch đăng bài"""
        return self.schedules

# Khởi tạo service
schedule_service = ScheduleService()