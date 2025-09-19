import json
import shutil
from datetime import datetime
from pathlib import Path
from database.json_manager import load_channels, load_sources, load_ads, load_schedules, load_posted
from utils.logger import logger

class BackupService:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self):
        """Tạo backup toàn bộ dữ liệu"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        backup_path.mkdir()
        
        # Backup tất cả dữ liệu
        data_to_backup = {
            'channels': load_channels(),
            'sources': load_sources(),
            'ads': load_ads(),
            'schedules': load_schedules(),
            'posted': load_posted()
        }
        
        for name, data in data_to_backup.items():
            with open(backup_path / f"{name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        return backup_path
    
    def list_backups(self):
        """Liệt kê tất cả backup"""
        backups = []
        for backup_dir in self.backup_dir.glob("backup_*"):
            if backup_dir.is_dir():
                backups.append({
                    'name': backup_dir.name,
                    'created_at': backup_dir.name.replace("backup_", ""),
                    'path': backup_dir
                })
        return sorted(backups, key=lambda x: x['created_at'], reverse=True)
    
    def restore_backup(self, backup_name):
        """Khôi phục từ backup"""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            return False
        
        # Restore dữ liệu
        from database.json_manager import save_channels, save_sources, save_ads, save_schedules, save_posted
        
        for file_path in backup_path.glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if file_path.name == "channels.json":
                save_channels(data)
            elif file_path.name == "sources.json":
                save_sources(data)
            elif file_path.name == "ads.json":
                save_ads(data)
            elif file_path.name == "schedules.json":
                save_schedules(data)
            elif file_path.name == "posted.json":
                save_posted(data)
        
        return True

# Khởi tạo service
backup_service = BackupService()