
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from ..db import Base
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    task_name = Column(String(150), nullable=False)
    args = JSONB
    status = Column(String(50))
    progress = Column(Integer, default=0)
    result = JSONB
    created_by = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
