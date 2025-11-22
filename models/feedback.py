from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum

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
