from datetime import datetime, timedelta
from typing import Any, Dict, Iterator
import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
# DatasetMemoryManager
#
# A drop-in replacement for the bare `datasets: Dict` global in main.py.
# Tracks last-accessed time per entry and automatically evicts stale datasets

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
