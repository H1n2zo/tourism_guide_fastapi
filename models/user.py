from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum

# ==================== USER MODEL ====================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100))
    role = Column(Enum("admin", "user"), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reviews = relationship("Review", back_populates="user")
    feedbacks = relationship("WebsiteFeedback", back_populates="user")
