
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from ..db import Base
class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    model_id = Column(Integer, ForeignKey("models.id"))
    severity = Column(String(20))
    ts = Column(DateTime(timezone=True))
    host = Column(String(255))
    app = Column(String(255))
    template_id = Column(String(255))
    message = Column(String)
    context = JSONB
    label = Column(String(10))
