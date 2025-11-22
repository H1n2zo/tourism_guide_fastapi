"""
Feedback API Endpoints
Website feedback and rating system
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from config.database import get_db
from models.feedback import WebsiteFeedback
from models.user import User
from schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from core.security import get_current_user, get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[FeedbackResponse])
async def get_feedback(
    is_public: Optional[bool] = None,
    is_read: Optional[bool] = None,
    category: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get all feedback with optional filtering
    """
    query = db.query(WebsiteFeedback)
    
    if is_public is not None:
        query = query.filter(WebsiteFeedback.is_public == is_public)
    
    if is_read is not None:
        query = query.filter(WebsiteFeedback.is_read == is_read)
    
    if category:
        query = query.filter(WebsiteFeedback.category == category)
    
    # Pagination
    offset = (page - 1) * page_size
    feedback_list = query.order_by(WebsiteFeedback.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()
    
    return feedback_list


@router.get("/public", response_model=List[FeedbackResponse])
async def get_public_feedback(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get public feedback for display on website
    """
    feedback_list = db.query(WebsiteFeedback)\
        .filter(WebsiteFeedback.is_public == True)\
        .order_by(WebsiteFeedback.created_at.desc())\
        .limit(limit)\
        .all()
    
    return feedback_list


@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback_by_id(
    feedback_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get single feedback by ID (Admin only)
    """
    feedback = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    return feedback


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = None
):
    """
    Submit website feedback (authentication optional)
    """
    # Validate rating
    if feedback.rating < 1 or feedback.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    # Create feedback
    new_feedback = WebsiteFeedback(
        user_id=current_user.id if current_user else None,
        user_name=feedback.user_name,
        email=feedback.email,
        rating=feedback.rating,
        category=feedback.category,
        feedback=feedback.feedback,
        is_public=True,  # Default to public
        is_read=False
    )
    
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    
    return new_feedback


@router.put("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: int,
    feedback: FeedbackUpdate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update feedback status (Admin only)
    """
    db_feedback = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.id == feedback_id
    ).first()
    
    if not db_feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Update fields
    for field, value in feedback.dict(exclude_unset=True).items():
        setattr(db_feedback, field, value)
    
    db.commit()
    db.refresh(db_feedback)
    
    return db_feedback


@router.put("/{feedback_id}/mark-read")
async def mark_feedback_read(
    feedback_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Mark feedback as read (Admin only)
    """
    feedback = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    feedback.is_read = True
    db.commit()
    
    return {
        "message": "Feedback marked as read",
        "success": True
    }


@router.put("/{feedback_id}/toggle-public")
async def toggle_feedback_public(
    feedback_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Toggle feedback public visibility (Admin only)
    """
    feedback = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    feedback.is_public = not feedback.is_public
    db.commit()
    
    return {
        "message": f"Feedback visibility changed to {'public' if feedback.is_public else 'private'}",
        "is_public": feedback.is_public,
        "success": True
    }


@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete feedback (Admin only)
    """
    feedback = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    db.delete(feedback)
    db.commit()
    
    return {
        "message": "Feedback deleted successfully",
        "success": True
    }


@router.get("/stats/overview")
async def get_feedback_stats(db: Session = Depends(get_db)):
    """
    Get feedback statistics
    """
    # Total feedback
    total_feedback = db.query(func.count(WebsiteFeedback.id)).scalar() or 0
    
    # Average rating
    avg_rating = db.query(func.avg(WebsiteFeedback.rating)).scalar()
    
    # Rating distribution
    rating_distribution = {}
    for rating in range(1, 6):
        count = db.query(func.count(WebsiteFeedback.id)).filter(
            WebsiteFeedback.rating == rating
        ).scalar() or 0
        rating_distribution[f"{rating}_star"] = count
    
    # Category distribution
    category_distribution = {}
    categories = ['usability', 'features', 'content', 'design', 'general']
    for category in categories:
        count = db.query(func.count(WebsiteFeedback.id)).filter(
            WebsiteFeedback.category == category
        ).scalar() or 0
        category_distribution[category] = count
    
    # Unread count
    unread_count = db.query(func.count(WebsiteFeedback.id)).filter(
        WebsiteFeedback.is_read == False
    ).scalar() or 0
    
    return {
        "total_feedback": total_feedback,
        "average_rating": round(avg_rating, 1) if avg_rating else 0.0,
        "rating_distribution": rating_distribution,
        "category_distribution": category_distribution,
        "unread_count": unread_count
    }


@router.get("/categories/list")
async def get_feedback_categories():
    """
    Get list of feedback categories
    """
    return {
        "categories": [
            {"value": "general", "label": "General Feedback"},
            {"value": "usability", "label": "Usability & Navigation"},
            {"value": "features", "label": "Features & Functionality"},
            {"value": "content", "label": "Content & Information"},
            {"value": "design", "label": "Design & Interface"}
        ]
    }