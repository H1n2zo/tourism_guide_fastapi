from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ==================== FEEDBACK SCHEMAS ====================
class FeedbackBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    category: str = Field(
        "general", 
        pattern="^(usability|features|content|design|general)$"
    )
    feedback: str = Field(..., min_length=10)


class FeedbackCreate(FeedbackBase):
    user_name: str = Field(..., max_length=100)
    email: Optional[EmailStr] = None


class FeedbackUpdate(BaseModel):
    is_public: Optional[bool] = None
    is_read: Optional[bool] = None


class FeedbackResponse(FeedbackBase):
    id: int
    user_id: Optional[int] = None
    user_name: str
    email: Optional[str] = None
    is_public: bool
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True