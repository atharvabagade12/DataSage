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
            print("✅ Tables created successfully!")
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

