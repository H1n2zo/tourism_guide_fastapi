from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.route import TransportMode

class RouteBase(BaseModel):
    route_name: Optional[str] = None
    origin_id: Optional[int] = None
    destination_id: Optional[int] = None
    transport_mode: TransportMode
    distance_km: Optional[Decimal] = None
    estimated_time_minutes: Optional[int] = None
    base_fare: Optional[Decimal] = None
    fare_per_km: Optional[Decimal] = None
    description: Optional[str] = None

class RouteCreate(RouteBase):
    pass

class RouteUpdate(RouteBase):
    is_active: Optional[bool] = True

class RouteResponse(RouteBase):
    id: int
    is_active: bool
    created_at: datetime
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    origin_lat: Optional[Decimal] = None
    origin_lng: Optional[Decimal] = None
    dest_lat: Optional[Decimal] = None
    dest_lng: Optional[Decimal] = None
    total_fare: Optional[float] = 0.0
    
    class Config:
        from_attributes = True