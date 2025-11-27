from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)

    datasets = relationship("Dataset", back_populates="owner")
    models = relationship("Model", back_populates="owner")

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    storage_path = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    row_count = Column(Integer)
    column_count = Column(Integer)
    size_bytes = Column(Integer)
    is_processed = Column(Boolean, default=False)
    parent_dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=True)
    
    owner = relationship("User", back_populates="datasets")
    models = relationship("Model", back_populates="dataset")
    children = relationship("Dataset")

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    name = Column(String)
    algorithm = Column(String)
    storage_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    metrics = Column(JSON)
    hyperparameters = Column(JSON)

    owner = relationship("User", back_populates="models")
    dataset = relationship("Dataset", back_populates="models")
