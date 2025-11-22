from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ==================== DESTINATION IMAGE SCHEMAS ====================
class DestinationImageBase(BaseModel):
    caption: Optional[str] = Field(None, max_length=200)
    is_primary: bool = False


class DestinationImageCreate(DestinationImageBase):
    destination_id: int
    image_path: str


class DestinationImageResponse(DestinationImageBase):
    id: int
    destination_id: int
    image_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True
