from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum

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
