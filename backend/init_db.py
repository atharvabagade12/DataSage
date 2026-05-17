from database import engine, Base
from models import User, Dataset, Model, UserAction
import time
import sys

def init_db(max_retries=5, retry_delay=2):
    """Initialize database with retry logic for Docker environments"""
    print("🔧 Creating database tables...")
    
    for attempt in range(1, max_retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            
            # Apply manual migrations for existing tables
            try:
                from sqlalchemy import text
                with engine.connect() as conn:
                    # SQLite support
                    if 'sqlite' in str(engine.url):
                        conn.execute(text("ALTER TABLE datasets ADD COLUMN data_version INTEGER NOT NULL DEFAULT 0;"))
                        conn.commit()
                    # PostgreSQL support
                    else:
                        conn.execute(text("ALTER TABLE datasets ADD COLUMN data_version INTEGER NOT NULL DEFAULT 0;"))
                        conn.commit()
            except Exception as ex:
                pass # Already exists or other error
            
            print("✅ Tables created and migrated successfully!")
            return True
        except Exception as e:
            if attempt < max_retries:
                print(f"⚠️  Attempt {attempt}/{max_retries} failed: {e}")
                print(f"   Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"❌ Error creating tables after {max_retries} attempts: {e}")
                return False
    
    return False

if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)

