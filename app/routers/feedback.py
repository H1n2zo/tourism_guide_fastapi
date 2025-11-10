from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models.review import WebsiteFeedback, FeedbackCategory
from app.models.user import User
from app.schemas.review import FeedbackCreate, FeedbackResponse
from app.services.auth_service import get_optional_user

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])

@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Submit website feedback"""
    db_feedback = WebsiteFeedback(
        user_id=current_user.id if current_user else None,
        user_name=feedback.user_name or (current_user.username if current_user else None),
        email=feedback.email,
        rating=feedback.rating,
        category=feedback.category,
        feedback=feedback.feedback,
        is_public=True
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return db_feedback

@router.get("/public", response_model=List[FeedbackResponse])
def get_public_feedback(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get public feedback"""
    feedbacks = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.is_public == True
    ).order_by(
        WebsiteFeedback.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return feedbacks

@router.get("/statistics")
def get_feedback_statistics(db: Session = Depends(get_db)):
    """Get feedback statistics"""
    total_feedback = db.query(func.count(WebsiteFeedback.id)).scalar()
    average_rating = db.query(func.avg(WebsiteFeedback.rating)).scalar()
    
    return {
        "total_feedback": total_feedback or 0,
        "average_rating": float(average_rating) if average_rating else 0.0
    }