# app/schemas/destination.py - Pydantic Schemas for Destinations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class DestinationImageBase(BaseModel):
    image_path: str
    caption: Optional[str] = None
    is_primary: bool = False


class DestinationImageResponse(DestinationImageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class DestinationBase(BaseModel):
    name: str = Field(..., max_length=200)
    category_id: Optional[int] = None
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    contact_number: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None, max_length=200)
    opening_hours: Optional[str] = Field(None, max_length=100)
    entry_fee: Optional[str] = Field(None, max_length=100)


class DestinationResponse(DestinationBase):
    id: int
    rating: Decimal
    image_path: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Related data
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    images: List[DestinationImageResponse] = []
    review_count: int = 0
    avg_rating: Optional[float] = None
    
    class Config:
        from_attributes = True


class DestinationListResponse(BaseModel):
    destinations: List[DestinationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int