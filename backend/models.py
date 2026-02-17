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
    column_metadata = Column(JSON, nullable=True) # stores semantic types and overrides
    
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

class UserAction(Base):
    __tablename__ = "user_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(String, nullable=False) # upload, train, preprocess, delete
    action_details = Column(JSON, nullable=True) # e.g. {"filename": "data.csv", "accuracy": 0.85}
    resource_id = Column(Integer, nullable=True) # ID of dataset or model
    resource_type = Column(String, nullable=True) # "dataset" or "model"
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="user_actions")

# Add relationship to User class
User.user_actions = relationship("UserAction", back_populates="user")
