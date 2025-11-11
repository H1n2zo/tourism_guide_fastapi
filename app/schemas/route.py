# app/schemas/route.py - Pydantic Schemas for Routes
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.route import TransportMode


class RouteResponse(BaseModel):
    id: int
    route_name: Optional[str]
    origin_id: Optional[int]
    destination_id: Optional[int]
    transport_mode: TransportMode
    distance_km: Optional[Decimal]
    estimated_time_minutes: Optional[int]
    base_fare: Optional[Decimal]
    fare_per_km: Optional[Decimal]
    description: Optional[str]
    is_active: bool
    created_at: datetime
    
    # Related data
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    origin_lat: Optional[Decimal] = None
    origin_lng: Optional[Decimal] = None
    dest_lat: Optional[Decimal] = None
    dest_lng: Optional[Decimal] = None
    total_fare: Optional[Decimal] = None
    
    class Config:
        from_attributes = True