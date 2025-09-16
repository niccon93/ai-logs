
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from ..db import Base
class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True)
    ts = Column(DateTime(timezone=True), nullable=False)
    host = Column(String(255))
    auid = Column(String(64))
    uid = Column(String(64))
    syscall = Column(String(64))
    exe = Column(String(512))
    comm = Column(String(255))
    success = Column(Boolean)
    path = Column(String(1024))
    action = Column(String(255))
    seinfo = JSONB
    raw = JSONB
