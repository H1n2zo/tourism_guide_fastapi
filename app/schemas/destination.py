from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)
    icon: Optional[str] = Field(None, max_length=50)

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Destination Image Schemas
class DestinationImageBase(BaseModel):
    image_path: str
    caption: Optional[str] = None
    is_primary: bool = False

class DestinationImageResponse(DestinationImageBase):
    id: int
    destination_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Destination Schemas
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

class DestinationCreate(DestinationBase):
    pass

class DestinationUpdate(DestinationBase):
    is_active: Optional[bool] = True

class DestinationResponse(DestinationBase):
    id: int
    rating: Decimal
    image_path: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    images: List[DestinationImageResponse] = []
    review_count: Optional[int] = 0
    avg_rating: Optional[float] = 0.0
    
    class Config:
        from_attributes = True

# Destination List Response (lighter version)
class DestinationListResponse(BaseModel):
    id: int
    name: str
    category_id: Optional[int]
    description: Optional[str]
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    rating: Decimal
    image_path: Optional[str]
    is_active: bool
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    review_count: int = 0
    avg_rating: Optional[float] = 0.0
    
    class Config:
        from_attributes = True