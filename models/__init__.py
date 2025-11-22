"""
Database Models for Tourism Guide FastAPI
Complete SQLAlchemy ORM models matching PHP database structure
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum


# ==================== USER MODEL ====================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100))
    role = Column(Enum("admin", "user"), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reviews = relationship("Review", back_populates="user")
    feedbacks = relationship("WebsiteFeedback", back_populates="user")


# ==================== CATEGORY MODEL ====================
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    destinations = relationship("Destination", back_populates="category")


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


# ==================== DESTINATION IMAGE MODEL ====================
class DestinationImage(Base):
    __tablename__ = "destination_images"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String(255), nullable=False)
    caption = Column(String(200))
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    destination = relationship("Destination", back_populates="images")


# ==================== REVIEW MODEL ====================
class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    user_name = Column(String(100))
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    destination = relationship("Destination", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


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


# ==================== FEEDBACK MODEL ====================
class FeedbackCategory(str, enum.Enum):
    usability = "usability"
    features = "features"
    content = "content"
    design = "design"
    general = "general"


class WebsiteFeedback(Base):
    __tablename__ = "website_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    user_name = Column(String(100))
    email = Column(String(100))
    rating = Column(Integer, nullable=False)  # 1-5
    category = Column(Enum(FeedbackCategory), default=FeedbackCategory.general)
    feedback = Column(Text, nullable=False)
    is_public = Column(Boolean, default=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="feedbacks")


# Note: Save this as models/__init__.py and import all models there
# from .user import User
# from .category import Category
# etc.