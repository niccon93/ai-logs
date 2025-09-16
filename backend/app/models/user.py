import enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum, DateTime, Boolean, text
from sqlalchemy.sql import func
from ..database import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    # match existing DB enum name; don't recreate type
    role = Column(
        SAEnum(RoleEnum, name="role_enum", create_type=False, validate_strings=True),
        nullable=False,
        server_default=text("'user'")
    )
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    mfa_enabled = Column(Boolean, nullable=False, server_default=text("false"))
    mfa_secret = Column(String, nullable=True)
