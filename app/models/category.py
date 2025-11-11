# app/models/category.py - Category Database Model
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    destinations = relationship("Destination", back_populates="category")