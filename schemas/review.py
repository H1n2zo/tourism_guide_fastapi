from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ==================== REVIEW SCHEMAS ====================
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    destination_id: int
    user_name: str = Field(..., max_length=100)


class ReviewUpdate(BaseModel):
    is_approved: bool

class ReviewResponse(ReviewBase):
    id: int
    destination_id: int
    user_id: Optional[int] = None
    user_name: str
    is_approved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True