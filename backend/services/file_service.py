import os
import shutil
from fastapi import UploadFile
from datetime import datetime
import pandas as pd
import io

STORAGE_ROOT = "storage"

class FileService:
    def __init__(self):
        # Ensure storage directories exist
        os.makedirs(os.path.join(STORAGE_ROOT, "datasets"), exist_ok=True)
        os.makedirs(os.path.join(STORAGE_ROOT, "models"), exist_ok=True)

    async def save_dataset(self, file: UploadFile, user_id: int) -> str:
        """Save uploaded dataset to disk"""
        user_dir = os.path.join(STORAGE_ROOT, "datasets", str(user_id), "raw")
        os.makedirs(user_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Clean filename
        safe_filename = "".join([c for c in file.filename if c.isalnum() or c in ('._- ')])
        filename = f"{timestamp}_{safe_filename}"
        file_path = os.path.join(user_dir, filename)
        
        # Reset file pointer
        await file.seek(0)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return file_path

    def save_dataframe(self, df: pd.DataFrame, user_id: int, filename: str, is_processed: bool = True) -> str:
        """Save pandas dataframe to disk (parquet recommended)"""
        subdir = "processed" if is_processed else "raw"
        user_dir = os.path.join(STORAGE_ROOT, "datasets", str(user_id), subdir)
        os.makedirs(user_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(user_dir, f"{timestamp}_{filename}.parquet")
        
        # Save as parquet for performance
        df.to_parquet(file_path, index=False)
        
        return file_path

    def load_dataframe(self, file_path: str) -> pd.DataFrame:
        """Load dataframe from disk"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.parquet'):
            return pd.read_parquet(file_path)
        else:
            raise ValueError("Unsupported file format")
