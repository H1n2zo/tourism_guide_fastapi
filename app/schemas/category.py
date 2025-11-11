# app/schemas/category.py - Pydantic Schemas for Categories
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryResponse(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    created_at: datetime
    destination_count: int = 0
    
    class Config:
        from_attributes = True