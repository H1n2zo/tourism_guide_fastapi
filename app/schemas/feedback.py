# app/schemas/feedback.py - Pydantic Schemas for Feedback
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.models.feedback import FeedbackCategory


class FeedbackCreate(BaseModel):
    user_name: str = Field(..., max_length=100)
    email: Optional[EmailStr] = None
    rating: int = Field(..., ge=1, le=5)
    category: FeedbackCategory = FeedbackCategory.GENERAL
    feedback: str = Field(..., min_length=10)


class FeedbackResponse(BaseModel):
    id: int
    user_name: Optional[str]
    email: Optional[str]
    rating: int
    category: FeedbackCategory
    feedback: str
    is_public: bool
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackStats(BaseModel):
    total_feedback: int
    average_rating: Optional[float]
    unread_count: int