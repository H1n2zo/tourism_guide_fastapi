# app/api/endpoints/feedback.py - FIXED Feedback API Endpoints
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.feedback import WebsiteFeedback, FeedbackCategory
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackStats

router = APIRouter()


@router.post("/", status_code=201)
async def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """Submit website feedback - FIXED"""
    try:
        # Handle enum conversion properly
        if isinstance(feedback.category, str):
            category_enum = FeedbackCategory(feedback.category.lower())
        else:
            category_enum = feedback.category
        
        db_feedback = WebsiteFeedback(
            user_name=feedback.user_name,
            email=feedback.email,
            rating=feedback.rating,
            category=category_enum,
            feedback=feedback.feedback,
            is_public=True,
            is_read=False
        )
        
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        
        return {
            "id": db_feedback.id,
            "user_name": db_feedback.user_name,
            "email": db_feedback.email,
            "rating": db_feedback.rating,
            "category": db_feedback.category.value,
            "feedback": db_feedback.feedback,
            "is_public": db_feedback.is_public,
            "is_read": db_feedback.is_read,
            "created_at": db_feedback.created_at.isoformat()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid category: {str(e)}")
    except Exception as e:
        db.rollback()
        print(f"Feedback submission error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")


@router.get("/public")
async def get_public_feedback(limit: int = 10, db: Session = Depends(get_db)):
    """Get public feedback for display - FIXED"""
    try:
        feedbacks = db.query(WebsiteFeedback).filter(
            WebsiteFeedback.is_public == True
        ).order_by(WebsiteFeedback.created_at.desc()).limit(limit).all()
        
        # Convert to JSON-serializable format
        result = []
        for fb in feedbacks:
            result.append({
                "id": fb.id,
                "user_name": fb.user_name,
                "email": fb.email,
                "rating": fb.rating,
                "category": fb.category.value,  # Convert enum to string
                "feedback": fb.feedback,
                "is_public": fb.is_public,
                "is_read": fb.is_read,
                "created_at": fb.created_at.isoformat()  # Convert datetime to string
            })
        
        return result
        
    except Exception as e:
        print(f"Error fetching feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_feedback_stats(db: Session = Depends(get_db)):
    """Get feedback statistics - FIXED"""
    try:
        total = db.query(func.count(WebsiteFeedback.id)).scalar() or 0
        
        avg_rating = db.query(func.avg(WebsiteFeedback.rating)).scalar()
        
        unread = db.query(func.count(WebsiteFeedback.id)).filter(
            WebsiteFeedback.is_read == False
        ).scalar() or 0
        
        return JSONResponse(content={
            "total_feedback": total,
            "average_rating": float(avg_rating) if avg_rating else None,
            "unread_count": unread
        })
        
    except Exception as e:
        print(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))