# app/models/user.py - User Database Model
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    reviews = relationship("Review", back_populates="user")
    feedbacks = relationship("WebsiteFeedback", back_populates="user")