# app/schemas/auth.py - Authentication Schemas
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserRegister(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT token"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: int
    username: str
    email: Optional[str]
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserWithToken(BaseModel):
    """Schema for login response with token"""
    user: UserResponse
    token: Token