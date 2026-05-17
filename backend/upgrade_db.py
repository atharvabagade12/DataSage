import os
import sqlalchemy
from sqlalchemy import text
from dotenv import load_dotenv

def upgrade_database():
    print("🚀 Upgrading database schema...")
    
    # Load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '.envs')
    load_dotenv(dotenv_path=env_path)
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not found in .envs")
        return

    print(f"🔗 Connecting to database: {db_url.split('@')[-1] if '@' in db_url else db_url}")
    
    try:
        engine = sqlalchemy.create_engine(db_url)
        with engine.connect() as conn:
            # Check if using Postgres
            if 'postgres' in db_url.lower():
                try:
                    print("Adding 'data_version' column to 'datasets' table in PostgreSQL...")
                    conn.execute(text("ALTER TABLE datasets ADD COLUMN data_version INTEGER NOT NULL DEFAULT 0;"))
                    conn.commit()
                    print("✅ Column added successfully.")
                except sqlalchemy.exc.ProgrammingError as e:
                    if 'already exists' in str(e).lower() or 'duplicate column' in str(e).lower():
                        print("ℹ️ 'data_version' column already exists.")
                    else:
                        raise e
            else:
                # SQLite fallback
                print("Adding 'data_version' column to 'datasets' table in SQLite...")
                try:
                    conn.execute(text("ALTER TABLE datasets ADD COLUMN data_version INTEGER NOT NULL DEFAULT 0;"))
                    conn.commit()
                    print("✅ Column added successfully.")
                except sqlalchemy.exc.OperationalError as e:
                    if 'duplicate column name' in str(e).lower():
                        print("ℹ️ 'data_version' column already exists.")
                    else:
                        raise e

        print("✅ Database upgrade complete.")
    except Exception as e:
        print(f"❌ Failed to upgrade database: {e}")

if __name__ == "__main__":
    upgrade_database()
