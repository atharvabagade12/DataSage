import os
import shutil
from fastapi import UploadFile
from datetime import datetime, timedelta
import pandas as pd
import io
import sys
from typing import Any, Dict, Iterator
from missing_value_markers import MISSING_VALUE_MARKERS

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
        safe_filename = "".join([c for c in file.filename if c.isalnum() or c in ("._- ")])
        filename = f"{timestamp}_{safe_filename}"
        file_path = os.path.join(user_dir, filename)

        await file.seek(0)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

    def save_dataframe(self, df: pd.DataFrame, user_id: int, filename: str, is_processed: bool = True) -> str:
        """Save pandas dataframe to disk (parquet)"""
        subdir = "processed" if is_processed else "raw"
        user_dir = os.path.join(STORAGE_ROOT, "datasets", str(user_id), subdir)
        os.makedirs(user_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(user_dir, f"{timestamp}_{filename}.parquet")
        df.to_parquet(file_path, index=False)
        return file_path

    def load_dataframe(self, file_path: str) -> pd.DataFrame:
        """Load dataframe from disk based on extension"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = file_path.lower()
        if ext.endswith(".csv"):
            return pd.read_csv(file_path, na_values=MISSING_VALUE_MARKERS, keep_default_na=True)
        elif ext.endswith(".parquet"):
            return pd.read_parquet(file_path)
        elif ext.endswith(".json"):
            return pd.read_json(file_path)
        elif ext.endswith(".xlsx") or ext.endswith(".xls"):
            return pd.read_excel(file_path, na_values=MISSING_VALUE_MARKERS, keep_default_na=True)
        else:
            raise ValueError(f"Unsupported file format: {os.path.basename(file_path)}")

    def get_storage_stats(self) -> dict:
        """Calculate disk usage of the storage directory"""
        total_bytes = 0
        raw_files = 0
        saved_versions = 0

        datasets_root = os.path.join(STORAGE_ROOT, "datasets")
        if os.path.exists(datasets_root):
            for root, _, files in os.walk(datasets_root):
                for f in files:
                    fpath = os.path.join(root, f)
                    try:
                        size = os.path.getsize(fpath)
                        total_bytes += size
                        if "processed" in root:
                            saved_versions += 1
                        elif "raw" in root:
                            raw_files += 1
                    except OSError:
                        pass

        return {
            "storage_root_mb": round(total_bytes / (1024 * 1024), 2),
            "total_raw_files": raw_files,
            "total_saved_versions": saved_versions,
        }


# ─────────────────────────────────────────────────────────────────────────────
# DatasetMemoryManager
#
# A drop-in replacement for the bare `datasets: Dict` global in main.py.
# Tracks last-accessed time per entry and automatically evicts stale datasets
# after `ttl_minutes` of inactivity.
#
# Exposes a FULL dict-compatible interface via dunder methods, so every existing
# `datasets[id]`, `if id in datasets`, `del datasets[id]`, `datasets.keys()`
# call in main.py continues to work with ZERO changes to those call sites.
# ─────────────────────────────────────────────────────────────────────────────

class DatasetMemoryManager:
    """
    TTL-based in-memory store for loaded pandas DataFrames.

    Wire into main.py like this (replaces the bare dict on line 159):

        from services.file_service import DatasetMemoryManager
        TTL = int(os.getenv("DATASET_TTL_MINUTES", "30"))
        datasets = DatasetMemoryManager(ttl_minutes=TTL)

    Then use *exactly* like the old dict — no other code needs to change.
    """

    def __init__(self, ttl_minutes: int = 30):
        self._store: Dict[str, dict] = {}
        self._access_times: Dict[str, datetime] = {}
        self.ttl_minutes = ttl_minutes

    # ── Core TTL operations ────────────────────────────────────────────────

    def get(self, dataset_id: str, default=None):
        """Return entry and refresh its access timestamp."""
        if dataset_id in self._store:
            self._access_times[dataset_id] = datetime.now()
            return self._store[dataset_id]
        return default

    def set(self, dataset_id: str, data: dict):
        """Store entry and set/refresh access timestamp."""
        self._store[dataset_id] = data
        self._access_times[dataset_id] = datetime.now()

    def delete(self, dataset_id: str):
        """Remove entry from memory (no-op if absent)."""
        self._store.pop(dataset_id, None)
        self._access_times.pop(dataset_id, None)

    def evict_stale(self) -> int:
        """
        Remove all entries idle longer than ttl_minutes.
        Called periodically by the background asyncio task in main.py.
        Returns count of evicted datasets.
        """
        cutoff = datetime.now() - timedelta(minutes=self.ttl_minutes)
        stale_ids = [k for k, t in self._access_times.items() if t < cutoff]
        for k in stale_ids:
            self._store.pop(k, None)
            self._access_times.pop(k, None)
            print(f"🗑️  [MemoryManager] Evicted dataset '{k}' from RAM "
                  f"(idle > {self.ttl_minutes} min)")
        return len(stale_ids)

    def total_memory_mb(self) -> float:
        """Estimate RAM used by stored DataFrames in MB."""
        total = 0
        for entry in self._store.values():
            df = entry.get("dataframe")
            if df is not None and hasattr(df, "memory_usage"):
                total += df.memory_usage(deep=True).sum()
        return round(total / (1024 * 1024), 2)

    def stats(self) -> dict:
        """Summary dict for the /api/health endpoint."""
        now = datetime.now()
        oldest_idle_mins = None
        if self._access_times:
            oldest_ts = min(self._access_times.values())
            oldest_idle_mins = round((now - oldest_ts).total_seconds() / 60, 1)
        return {
            "datasets_in_ram": len(self._store),
            "estimated_mb": self.total_memory_mb(),
            "oldest_idle_mins": oldest_idle_mins,
            "ttl_minutes": self.ttl_minutes,
        }

    # ── Full dict-compatible interface ────────────────────────────────────

    def __contains__(self, key: str) -> bool:
        return key in self._store

    def __getitem__(self, key: str) -> dict:
        if key not in self._store:
            raise KeyError(key)
        self._access_times[key] = datetime.now()
        return self._store[key]

    def __setitem__(self, key: str, value: dict):
        self.set(key, value)

    def __delitem__(self, key: str):
        if key not in self._store:
            raise KeyError(key)
        self.delete(key)

    def __len__(self) -> int:
        return len(self._store)

    def __iter__(self) -> Iterator[str]:
        return iter(self._store)

    def keys(self):
        return self._store.keys()

    def values(self):
        return self._store.values()

    def items(self):
        return self._store.items()

    def pop(self, key: str, *args):
        self._access_times.pop(key, None)
        return self._store.pop(key, *args)
