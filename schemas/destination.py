from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ==================== DESTINATION SCHEMAS ====================
class DestinationBase(BaseModel):
    name: str = Field(..., max_length=200)
    category_id: Optional[int] = None
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    contact_number: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(None, max_length=200)
    opening_hours: Optional[str] = Field(None, max_length=100)
    entry_fee: Optional[str] = Field(None, max_length=100)


class DestinationCreate(DestinationBase):
    is_active: bool = True


class DestinationUpdate(DestinationBase):
    is_active: Optional[bool] = None


class DestinationResponse(DestinationBase):
    id: int
    rating: Optional[Decimal] = None
    image_path: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Nested data
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    review_count: Optional[int] = 0
    avg_rating: Optional[float] = None
    
    class Config:
        from_attributes = True

