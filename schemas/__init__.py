"""
Pydantic Schemas for Tourism Guide FastAPI
Request/Response validation and serialization
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ==================== USER SCHEMAS ====================
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ==================== CATEGORY SCHEMAS ====================
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)
    icon: Optional[str] = Field(None, max_length=50)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


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


# ==================== DESTINATION IMAGE SCHEMAS ====================
class DestinationImageBase(BaseModel):
    caption: Optional[str] = Field(None, max_length=200)
    is_primary: bool = False


class DestinationImageCreate(DestinationImageBase):
    destination_id: int
    image_path: str


class DestinationImageResponse(DestinationImageBase):
    id: int
    destination_id: int
    image_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True


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


# ==================== ROUTE SCHEMAS ====================
class RouteBase(BaseModel):
    route_name: Optional[str] = Field(None, max_length=200)
    origin_id: int
    destination_id: int
    transport_mode: str = Field(..., pattern="^(jeepney|taxi|bus|van|tricycle|walking)$")
    distance_km: Optional[Decimal] = None
    estimated_time_minutes: Optional[int] = None
    base_fare: Optional[Decimal] = None
    fare_per_km: Optional[Decimal] = None
    description: Optional[str] = None


class RouteCreate(RouteBase):
    is_active: bool = True


class RouteUpdate(RouteBase):
    is_active: Optional[bool] = None


class RouteResponse(RouteBase):
    id: int
    is_active: bool
    created_at: datetime
    
    # Nested data
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    origin_lat: Optional[Decimal] = None
    origin_lng: Optional[Decimal] = None
    dest_lat: Optional[Decimal] = None
    dest_lng: Optional[Decimal] = None
    total_fare: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


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


# ==================== PAGINATION SCHEMA ====================
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    search: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None


class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @validator('total_pages', always=True)
    def calculate_total_pages(cls, v, values):
        total = values.get('total', 0)
        page_size = values.get('page_size', 10)
        return (total + page_size - 1) // page_size if page_size > 0 else 0


# ==================== STATISTICS SCHEMA ====================
class StatisticsResponse(BaseModel):
    total_destinations: int = 0
    total_reviews: int = 0
    total_categories: int = 0
    total_routes: int = 0
    total_users: int = 0
    avg_rating: Optional[float] = None


# ==================== FILE UPLOAD SCHEMA ====================
class FileUploadResponse(BaseModel):
    success: bool
    filename: str
    path: str
    url: str
    message: Optional[str] = None