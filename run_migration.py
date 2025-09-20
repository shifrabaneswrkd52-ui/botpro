# run_migration.py
import sys
from pathlib import Path

# Thêm đường dẫn hiện tại
sys.path.append(str(Path(__file__).parent))

from database.migrate_data import migrate_json_to_db

if __name__ == "__main__":
    migrate_json_to_db()