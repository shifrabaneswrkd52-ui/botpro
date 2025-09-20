from sqlalchemy.orm import Session
from database.config import SessionLocal
from database.models import Schedule
from utils.logger import logger

class ScheduleService:
    def __init__(self):
        self.db = SessionLocal()
        self.schedules = self.load_schedules()
    
    def load_schedules(self):
        """Tải schedules từ database"""
        return {schedule.id: {
            'channel_id': schedule.channel_id,
            'interval_seconds': schedule.interval_seconds,
            'enabled': schedule.enabled,
            'last_run': schedule.last_run,
            'next_run': schedule.next_run,
            'created_at': schedule.created_at
        } for schedule in self.db.query(Schedule).all()}
    
    def add_schedule(self, channel_id, interval_seconds, enabled=True):
        """Thêm lịch đăng bài mới"""
        try:
            schedule = Schedule(
                channel_id=channel_id,
                interval_seconds=interval_seconds,
                enabled=enabled
            )
            self.db.add(schedule)
            self.db.commit()
            self.db.refresh(schedule)
            
            # Cập nhật cache
            self.schedules[schedule.id] = {
                'channel_id': schedule.channel_id,
                'interval_seconds': schedule.interval_seconds,
                'enabled': schedule.enabled,
                'last_run': schedule.last_run,
                'next_run': schedule.next_run,
                'created_at': schedule.created_at
            }
            
            return schedule.id
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding schedule: {e}")
            return None
    
    def update_schedule(self, schedule_id, **kwargs):
        """Cập nhật lịch đăng bài"""
        try:
            schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if schedule:
                for key, value in kwargs.items():
                    setattr(schedule, key, value)
                self.db.commit()
                
                # Cập nhật cache
                if schedule_id in self.schedules:
                    self.schedules[schedule_id].update(kwargs)
                
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating schedule: {e}")
            return False
    
    def delete_schedule(self, schedule_id):
        """Xóa lịch đăng bài"""
        try:
            schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if schedule:
                self.db.delete(schedule)
                self.db.commit()
                
                # Xóa khỏi cache
                if schedule_id in self.schedules:
                    del self.schedules[schedule_id]
                
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting schedule: {e}")
            return False
    
    def get_channel_schedules(self, channel_id):
        """Lấy lịch đăng bài của kênh"""
        return {k: v for k, v in self.schedules.items() if v['channel_id'] == channel_id}
    
    def get_all_schedules(self):
        """Lấy tất cả lịch đăng bài"""
        return self.schedules

# Khởi tạo service
schedule_service = ScheduleService()