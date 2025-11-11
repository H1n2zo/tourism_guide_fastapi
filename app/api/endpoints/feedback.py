# app/api/endpoints/feedback.py - Feedback API Endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.feedback import WebsiteFeedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackStats

router = APIRouter()


@router.post("/", response_model=FeedbackResponse, status_code=201)
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """Submit website feedback"""
    
    db_feedback = WebsiteFeedback(
        user_name=feedback.user_name,
        email=feedback.email,
        rating=feedback.rating,
        category=feedback.category,
        feedback=feedback.feedback,
        is_public=True,
        is_read=False
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return db_feedback


@router.get("/public", response_model=List[FeedbackResponse])
def get_public_feedback(limit: int = 10, db: Session = Depends(get_db)):
    """Get public feedback for display on feedback page"""
    
    feedbacks = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.is_public == True
    ).order_by(WebsiteFeedback.created_at.desc()).limit(limit).all()
    
    return feedbacks


@router.get("/stats", response_model=FeedbackStats)
def get_feedback_stats(db: Session = Depends(get_db)):
    """Get feedback statistics"""
    
    total = db.query(func.count(WebsiteFeedback.id)).scalar()
    
    avg_rating = db.query(func.avg(WebsiteFeedback.rating)).scalar()
    
    unread = db.query(func.count(WebsiteFeedback.id)).filter(
        WebsiteFeedback.is_read == False
    ).scalar()
    
    return FeedbackStats(
        total_feedback=total or 0,
        average_rating=float(avg_rating) if avg_rating else None,
        unread_count=unread or 0
    )