# app/models/review_image.py - Review Image Model
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ReviewImage(Base):
    __tablename__ = "review_images"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    review = relationship("Review", back_populates="images")