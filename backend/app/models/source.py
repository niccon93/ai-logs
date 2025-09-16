
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from ..db import Base
import enum
class SourceType(str, enum.Enum):
    local="local"; ssh="ssh"; syslog="syslog"; journal="journal"; auditd="auditd"
class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(SourceType), nullable=False)
    path = Column(String(1024))
    server_account_id = Column(Integer, ForeignKey("server_accounts.id"), nullable=True)
    tags = Column(JSONB, default=dict)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True))
