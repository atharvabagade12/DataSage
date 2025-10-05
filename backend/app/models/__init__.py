from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for proper table creation
from .user import User
from .trained_models import TrainedModel
from .user_action import UserAction
from .model_performance import ModelPerformance
