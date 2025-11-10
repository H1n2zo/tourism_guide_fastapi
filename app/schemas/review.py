from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.models.review import FeedbackCategory

# Review Schemas
class ReviewBase(BaseModel):
    destination_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    user_name: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    is_approved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Website Feedback Schemas
class FeedbackBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    category: FeedbackCategory = FeedbackCategory.GENERAL
    feedback: str = Field(..., min_length=10)

class FeedbackCreate(FeedbackBase):
    user_name: str
    email: Optional[EmailStr] = None

class FeedbackResponse(FeedbackBase):
    id: int
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    email: Optional[str] = None
    is_public: bool
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        