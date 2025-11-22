from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

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