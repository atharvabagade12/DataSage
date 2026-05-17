import os
import sqlalchemy
from sqlalchemy import text
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.envs')
load_dotenv(dotenv_path=env_path)

db_url = os.getenv("DATABASE_URL")
engine = sqlalchemy.create_engine(db_url)
with engine.connect() as conn:
    try:
        # Check columns
        if 'postgres' in db_url.lower():
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='datasets';"))
            cols = [row[0] for row in result]
            print(f"Columns in datasets table: {cols}")
        else:
            result = conn.execute(text("PRAGMA table_info(datasets);"))
            cols = [row[1] for row in result]
            print(f"Columns in datasets table: {cols}")
    except Exception as e:
        print(f"Error checking columns: {e}")
