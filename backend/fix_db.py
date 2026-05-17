import os
import psycopg2
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.envs')
load_dotenv(dotenv_path=env_path)

db_url = os.getenv("DATABASE_URL")
print(f"Connecting to: {db_url.split('@')[-1] if '@' in db_url else db_url}")

try:
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='datasets' AND column_name='data_version';
    """)
    if cursor.fetchone():
        print("ℹ️ Column 'data_version' definitely exists according to information_schema.")
    else:
        print("Column 'data_version' missing. Adding it now...")
        cursor.execute("ALTER TABLE datasets ADD COLUMN data_version INTEGER NOT NULL DEFAULT 0;")
        print("✅ Column added successfully.")
        
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
