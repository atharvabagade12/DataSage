import os
import io
from datetime import datetime
from fastapi import UploadFile
import pandas as pd
from dotenv import load_dotenv
from missing_value_markers import MISSING_VALUE_MARKERS

# Load .envs so SUPABASE_URL / SUPABASE_SERVICE_KEY are available even when
# this module is imported before database.py runs load_dotenv().
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".envs"))

# ─────────────────────────────────────────────────────────────────────────────
# SupabaseStorageService
#
# Drop-in replacement for FileService. Uses Supabase Storage (S3-compatible)
# to persist all user datasets and saved versions.
#
# Key design decisions:
# - save_dataset()   → uploads raw file, returns (bucket_key, size_bytes)
# - load_dataframe() → downloads from Supabase, parses into DataFrame
# - save_dataframe() → serialises DataFrame → parquet, uploads to Supabase
# - delete_file()    → removes a file from the bucket
# - get_storage_stats() → best-effort stats (kept for /api/health compat.)
#
# The bucket key (e.g.  "user_5/raw/20260428_iris.csv") is stored in the DB
# `storage_path` column instead of a local OS path. All existing load sites
# in main.py that call `file_service.load_dataframe(dataset.storage_path)`
# continue to work without any changes at those call sites.
# ─────────────────────────────────────────────────────────────────────────────

BUCKET = "datasets"


def _get_supabase_client():
    """Lazy-initialise Supabase client (avoids import at module level crashing
    the app when env vars are missing during local dev without Supabase)."""
    from supabase import create_client
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_SERVICE_KEY", "").strip()
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in your .envs file."
        )
    return create_client(url, key)


class SupabaseStorageService:
    """Supabase Storage-backed file service for DataSage datasets."""

    def __init__(self):
        self._client = None  # Lazily initialised on first use

    @property
    def client(self):
        if self._client is None:
            self._client = _get_supabase_client()
        return self._client

    # ── Upload ────────────────────────────────────────────────────────────────

    async def save_dataset(self, file: UploadFile, user_id: int):
        """
        Upload a user-submitted file to Supabase Storage.

        Returns:
            (bucket_key: str, size_bytes: int)
            bucket_key is stored in the DB as `storage_path`.
        """
        await file.seek(0)
        file_bytes = await file.read()
        size_bytes = len(file_bytes)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(
            c for c in (file.filename or "upload") if c.isalnum() or c in "._- "
        )
        bucket_key = f"user_{user_id}/raw/{timestamp}_{safe_name}"

        self.client.storage.from_(BUCKET).upload(
            path=bucket_key,
            file=file_bytes,
            file_options={"content-type": "application/octet-stream", "upsert": "true"},
        )
        print(f"☁️  [Supabase] Uploaded → {bucket_key} ({size_bytes:,} bytes)")
        return bucket_key, size_bytes

    # ── Download / Load ───────────────────────────────────────────────────────

    def load_dataframe(self, bucket_key: str) -> pd.DataFrame:
        """
        Download a file from Supabase Storage and parse it into a DataFrame.

        Raises FileNotFoundError if the key does not exist in the bucket
        (so existing `except FileNotFoundError` blocks in main.py still work).
        """
        try:
            file_bytes: bytes = self.client.storage.from_(BUCKET).download(bucket_key)
        except Exception as exc:
            # Supabase raises generic exceptions; surface as FileNotFoundError
            # so callers in main.py can handle it uniformly.
            raise FileNotFoundError(
                f"Dataset not found in Supabase Storage (key={bucket_key}): {exc}"
            ) from exc

        buffer = io.BytesIO(file_bytes)
        key_lower = bucket_key.lower()

        if key_lower.endswith(".csv"):
            return pd.read_csv(buffer, na_values=MISSING_VALUE_MARKERS, keep_default_na=True)
        elif key_lower.endswith(".parquet"):
            return pd.read_parquet(buffer)
        elif key_lower.endswith(".json"):
            return pd.read_json(buffer)
        elif key_lower.endswith(".xlsx") or key_lower.endswith(".xls"):
            return pd.read_excel(buffer, na_values=MISSING_VALUE_MARKERS, keep_default_na=True)
        else:
            # Default fallback: try CSV
            buffer.seek(0)
            return pd.read_csv(buffer, na_values=MISSING_VALUE_MARKERS, keep_default_na=True)

    # ── Save DataFrame (versions / processed files) ───────────────────────────

    def save_dataframe(
        self,
        df: pd.DataFrame,
        user_id: int,
        filename: str,
        is_processed: bool = True,
    ) -> str:
        """
        Serialise a DataFrame to Parquet and upload to Supabase.

        Returns the bucket key (stored in the DB as `storage_path`).
        """
        subdir = "processed" if is_processed else "raw"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bucket_key = f"user_{user_id}/{subdir}/{timestamp}_{filename}.parquet"

        buf = io.BytesIO()
        df.to_parquet(buf, index=False)
        buf.seek(0)
        parquet_bytes = buf.read()

        self.client.storage.from_(BUCKET).upload(
            path=bucket_key,
            file=parquet_bytes,
            file_options={"content-type": "application/octet-stream", "upsert": "true"},
        )
        print(f"☁️  [Supabase] Saved DataFrame → {bucket_key} ({len(parquet_bytes):,} bytes)")
        return bucket_key

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete_file(self, bucket_key: str):
        """Remove a single file from Supabase Storage. Non-fatal on error."""
        if not bucket_key:
            return
        try:
            self.client.storage.from_(BUCKET).remove([bucket_key])
            print(f"🗑️  [Supabase] Deleted → {bucket_key}")
        except Exception as exc:
            print(f"⚠️  [Supabase] Could not delete '{bucket_key}': {exc}")

    # ── Stats (kept for /api/health compatibility) ────────────────────────────

    def get_storage_stats(self) -> dict:
        """
        Return storage statistics.
        Supabase free tier doesn't expose per-file sizes easily, so we return
        zero-values to keep the /api/health endpoint happy.
        """
        try:
            # List top-level folders (best effort)
            items = self.client.storage.from_(BUCKET).list()
            total_files = len(items) if isinstance(items, list) else 0
        except Exception:
            total_files = 0

        return {
            "storage_root_mb": 0.0,
            "total_raw_files": total_files,
            "total_saved_versions": 0,
            "backend": "supabase",
        }
