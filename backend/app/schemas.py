from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    role: Literal["admin","user"]
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: Optional[EmailStr] = None
    password: str = Field(min_length=6)
    role: Literal["admin","user"] = "user"

class ServerAccountIn(BaseModel):
    name: str
    username: str
    public_key: Optional[str] = None
    description: Optional[str] = None

class SourceIn(BaseModel):
    server_account_id: int
    path_glob: str
    interval_minutes: int = 5
    enabled: bool = True

class SourceOut(BaseModel):
    id: int
    server_account_id: int
    path_glob: str
    interval_minutes: int
    enabled: bool
    class Config:
        from_attributes = True

class ServerAccountOut(BaseModel):
    id: int
    name: str
    username: str
    public_key: Optional[str]
    description: Optional[str]
    class Config:
        from_attributes = True
