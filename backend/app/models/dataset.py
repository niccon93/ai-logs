
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..db import Base
class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    status = Column(String(50))
    total_lines = Column(Integer)
    parsed_lines = Column(Integer)
    parser = Column(String(50))
    schema_version = Column(String(20))
    s3_uri = Column(String(1024))
    created_at = Column(DateTime(timezone=True))
