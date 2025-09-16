
from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary, Enum, ForeignKey
from ..db import Base
import enum
class AuthType(str, enum.Enum):
    password="password"; ssh_key="ssh_key"
class ServerAccount(Base):
    __tablename__ = "server_accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(Integer, default=22, nullable=False)
    username = Column(String(150), nullable=False)
    auth_type = Column(Enum(AuthType), nullable=False)
    enc_password = Column(LargeBinary, nullable=True)
    enc_private_key = Column(LargeBinary, nullable=True)
    key_fingerprint = Column(String(255))
    verified_at = Column(DateTime(timezone=True))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    disabled = Column(Boolean, default=False)
