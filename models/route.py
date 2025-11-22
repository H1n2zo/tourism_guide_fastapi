from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum

# ==================== ROUTE MODEL ====================
class TransportMode(str, enum.Enum):
    jeepney = "jeepney"
    taxi = "taxi"
    bus = "bus"
    van = "van"
    tricycle = "tricycle"
    walking = "walking"

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String(200))
    origin_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"))
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"))
    transport_mode = Column(Enum(TransportMode), nullable=False)
    distance_km = Column(Numeric(6, 2))
    estimated_time_minutes = Column(Integer)
    base_fare = Column(Numeric(8, 2))
    fare_per_km = Column(Numeric(8, 2))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    origin = relationship("Destination", foreign_keys=[origin_id], back_populates="origin_routes")
    destination_point = relationship("Destination", foreign_keys=[destination_id], back_populates="destination_routes")
