# app/models/route.py - Route Database Model (FIXED)
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class TransportMode(str, enum.Enum):
    """Transport modes - MUST match database enum values"""
    JEEPNEY = "jeepney"
    TAXI = "taxi"
    BUS = "bus"
    VAN = "van"
    TRICYCLE = "tricycle"
    WALKING = "walking"


class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String(200), nullable=True)
    origin_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=True)
    transport_mode = Column(Enum(TransportMode), nullable=False)
    distance_km = Column(Numeric(6, 2), nullable=True)
    estimated_time_minutes = Column(Integer, nullable=True)
    base_fare = Column(Numeric(8, 2), nullable=True)
    fare_per_km = Column(Numeric(8, 2), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    origin = relationship("Destination", foreign_keys=[origin_id])
    destination = relationship("Destination", foreign_keys=[destination_id])