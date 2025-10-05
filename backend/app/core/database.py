from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from .config import settings

# Database URL from environment or settings
DATABASE_URL = settings.database_url

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database - create all tables
def init_db():
    from app.models import Base  # Import all models
    Base.metadata.create_all(bind=engine)
    print("✅ SQLAlchemy tables created successfully!")
