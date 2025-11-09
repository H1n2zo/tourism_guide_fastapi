# config/database.py
"""
Database Configuration for FastAPI Tourism Guide System
Connects to MySQL/MariaDB via XAMPP
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, Boolean, DateTime, Enum, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Generator
import os
from pathlib import Path

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")  # Default XAMPP password is empty
DB_NAME = os.getenv("DB_NAME", "tourism_guide")
DB_PORT = os.getenv("DB_PORT", "3306")

# Create Database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # Set to True for SQL query debugging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Base URL Configuration
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/")
UPLOAD_PATH = Path(__file__).parent.parent / "uploads"
UPLOAD_URL = f"{BASE_URL}uploads/"

# Create uploads directory if it doesn't exist
UPLOAD_PATH.mkdir(exist_ok=True)
(UPLOAD_PATH / "destinations").mkdir(exist_ok=True)
(UPLOAD_PATH / "categories").mkdir(exist_ok=True)

# Map Provider - FREE Leaflet/OpenStreetMap
MAP_PROVIDER = "leaflet"


# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100))
    role = Column(Enum('admin', 'user'), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category_id = Column(Integer)
    description = Column(Text)
    address = Column(Text)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    contact_number = Column(String(50))
    email = Column(String(100))
    website = Column(String(200))
    opening_hours = Column(String(100))
    entry_fee = Column(String(100))
    rating = Column(DECIMAL(2, 1), default=0.0)
    image_path = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DestinationImage(Base):
    __tablename__ = "destination_images"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, nullable=False)
    image_path = Column(String(255), nullable=False)
    caption = Column(String(200))
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, nullable=False)
    user_id = Column(Integer)
    user_name = Column(String(100))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String(200))
    origin_id = Column(Integer)
    destination_id = Column(Integer)
    transport_mode = Column(Enum('jeepney', 'taxi', 'bus', 'van', 'tricycle', 'walking'), nullable=False)
    distance_km = Column(DECIMAL(6, 2))
    estimated_time_minutes = Column(Integer)
    base_fare = Column(DECIMAL(8, 2))
    fare_per_km = Column(DECIMAL(8, 2))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class WebsiteFeedback(Base):
    __tablename__ = "website_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_name = Column(String(100))
    email = Column(String(100))
    rating = Column(Integer, nullable=False)
    category = Column(Enum('usability', 'features', 'content', 'design', 'general'), default='general')
    feedback = Column(Text, nullable=False)
    is_public = Column(Boolean, default=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI endpoints
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper function to create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


# Helper function to test database connection
def test_connection():
    """Test database connection"""
    try:
        db = SessionLocal()
        # Fixed: Use text() wrapper for SQL expressions
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False