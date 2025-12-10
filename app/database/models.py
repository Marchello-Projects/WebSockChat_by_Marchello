from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from enum import Enum
from app.config.configdb import Base

class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default=UserRole.USER.value)