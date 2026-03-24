import os
from dotenv import load_dotenv
load_dotenv('.envs')
from database import SessionLocal
from models import Dataset, Model

# Setup DB connection
db = SessionLocal()

print("Starting storage cleanup...")

# Get active paths from DB
active_dataset_paths = [os.path.normpath(d.storage_path) for d in db.query(Dataset).all() if d.storage_path]
active_model_paths = [os.path.normpath(m.storage_path) for m in db.query(Model).all() if m.storage_path]
active_paths = set(active_dataset_paths + active_model_paths)

print(f"Found {len(active_paths)} active files in the database.")

# Walk through storage directory
storage_root = "storage"
deleted_files = 0
freed_bytes = 0

if os.path.exists(storage_root):
    for root, dirs, files in os.walk(storage_root):
        for filename in files:
            file_path = os.path.join(root, filename)
            normalized_path = os.path.normpath(file_path)
            
            # If the file is not recorded in the DB, it's an orphan
            if normalized_path not in active_paths:
                try:
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_files += 1
                    freed_bytes += size
                    print(f"Deleted orphaned file: {file_path}")
                except Exception as e:
                    print(f"Could not delete {file_path}: {e}")

freed_mb = freed_bytes / (1024 * 1024)
print(f"Cleanup Complete! Deleted {deleted_files} orphaned files, freeing {freed_mb:.2f} MB of disk space.")
