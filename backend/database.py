from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get DB URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with retry logic for Docker environments
# pool_pre_ping=True helps handle DB connection drops
# pool_recycle=3600 recycles connections after 1 hour
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10,
        "options": "-c timezone=utc"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
