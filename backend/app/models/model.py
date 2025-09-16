
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from ..db import Base
import enum
class Framework(str, enum.Enum):
    logai="logai"; loglizer="loglizer"; deeploglizer="deeploglizer"; custom="custom"
class MLModel(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    framework = Column(Enum(Framework), nullable=False)
    params = JSONB
    metrics = JSONB
    artifact_uri = Column(String(1024))
    created_at = Column(DateTime(timezone=True))
