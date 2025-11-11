# app/schemas/review.py - Pydantic Schemas for Reviews
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    destination_id: int
    user_name: str = Field(..., max_length=100)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    destination_id: int
    user_name: Optional[str]
    rating: int
    comment: Optional[str]
    is_approved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReviewStats(BaseModel):
    destination_id: int
    total_reviews: int
    average_rating: Optional[float]
    five_star: int
    four_star: int
    three_star: int
    two_star: int
    one_star: int