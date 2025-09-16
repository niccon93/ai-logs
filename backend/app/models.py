from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.user)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class ServerAccount(Base):
    __tablename__ = "server_accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    username = Column(String(128), nullable=False)
    public_key = Column(Text, nullable=True)  # id_rsa.pub contents
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    sources = relationship("Source", back_populates="server_account", cascade="all,delete")

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    server_account_id = Column(Integer, ForeignKey("server_accounts.id"), nullable=False)
    path_glob = Column(String(512), nullable=False)  # /var/log/*.log
    interval_minutes = Column(Integer, default=5, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    server_account = relationship("ServerAccount", back_populates="sources")
