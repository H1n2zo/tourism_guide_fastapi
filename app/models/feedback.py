# app/models/feedback.py - Website Feedback Model (FIXED)
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class FeedbackCategory(str, enum.Enum):
    USABILITY = "usability"
    FEATURES = "features"
    CONTENT = "content"
    DESIGN = "design"
    GENERAL = "general"


class WebsiteFeedback(Base):
    __tablename__ = "website_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    rating = Column(Integer, nullable=False)
    category = Column(Enum(FeedbackCategory), default=FeedbackCategory.GENERAL)
    feedback = Column(Text, nullable=False)
    is_public = Column(Boolean, default=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_feedback_rating_range'),
    )
    
    # Relationships
    user = relationship("User", back_populates="feedbacks")