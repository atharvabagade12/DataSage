from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class TrainedModel(Base):
    __tablename__ = "trained_models"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_name = Column(String, nullable=False)
    algorithm = Column(String, nullable=False)
    algorithm_type = Column(String, nullable=False)
    parameters = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    dataset_info = Column(JSON, nullable=True)
    model_data = Column(LargeBinary, nullable=True)  # Binary field for serialized model
    training_time = Column(Float, nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="trained_models")
    performance_metrics = relationship("ModelPerformance", back_populates="model", cascade="all, delete-orphan")
