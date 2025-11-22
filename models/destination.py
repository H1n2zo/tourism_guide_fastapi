from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum


# ==================== DESTINATION MODEL ====================
class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    description = Column(Text)
    address = Column(Text)
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    contact_number = Column(String(50))
    email = Column(String(100))
    website = Column(String(200))
    opening_hours = Column(String(100))
    entry_fee = Column(String(100))
    rating = Column(Numeric(2, 1), default=0.0)
    image_path = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="destinations")
    images = relationship("DestinationImage", back_populates="destination", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="destination", cascade="all, delete-orphan")
    origin_routes = relationship("Route", foreign_keys="Route.origin_id", back_populates="origin")
    destination_routes = relationship("Route", foreign_keys="Route.destination_id", back_populates="destination_point")
