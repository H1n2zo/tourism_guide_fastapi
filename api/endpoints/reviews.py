"""
Review API Endpoints
CRUD operations for destination reviews
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from config.database import get_db
from models.review import Review
from models.destination import Destination
from models.user import User
from schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from core.security import get_current_user, get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(
    destination_id: Optional[int] = None,
    is_approved: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get all reviews with optional filtering
    """
    query = db.query(Review)
    
    if destination_id:
        query = query.filter(Review.destination_id == destination_id)
    
    if is_approved is not None:
        query = query.filter(Review.is_approved == is_approved)
    
    # Pagination
    offset = (page - 1) * page_size
    reviews = query.order_by(Review.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()
    
    return reviews


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: Session = Depends(get_db)):
    """
    Get single review by ID
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    return review


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = None
):
    """
    Submit a new review (authentication optional)
    """
    # Verify destination exists
    destination = db.query(Destination).filter(
        Destination.id == review.destination_id
    ).first()
    
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    # Create review
    new_review = Review(
        destination_id=review.destination_id,
        user_id=current_user.id if current_user else None,
        user_name=review.user_name,
        rating=review.rating,
        comment=review.comment,
        is_approved=True  # Auto-approve by default
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    # Update destination average rating
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.destination_id == review.destination_id,
        Review.is_approved == True
    ).scalar()
    
    destination.rating = round(avg_rating, 1) if avg_rating else 0.0
    db.commit()
    
    return new_review


@router.put("/{review_id}/approve", response_model=ReviewResponse)
async def approve_review(
    review_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Approve a review (Admin only)
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    review.is_approved = True
    db.commit()
    db.refresh(review)
    
    # Update destination rating
    destination = db.query(Destination).filter(
        Destination.id == review.destination_id
    ).first()
    
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.destination_id == review.destination_id,
        Review.is_approved == True
    ).scalar()
    
    destination.rating = round(avg_rating, 1) if avg_rating else 0.0
    db.commit()
    
    return review


@router.put("/{review_id}/reject", response_model=ReviewResponse)
async def reject_review(
    review_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Reject a review (Admin only)
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    review.is_approved = False
    db.commit()
    db.refresh(review)
    
    # Update destination rating
    destination = db.query(Destination).filter(
        Destination.id == review.destination_id
    ).first()
    
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.destination_id == review.destination_id,
        Review.is_approved == True
    ).scalar()
    
    destination.rating = round(avg_rating, 1) if avg_rating else 0.0
    db.commit()
    
    return review


@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a review (Admin only)
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    destination_id = review.destination_id
    
    db.delete(review)
    db.commit()
    
    # Update destination rating
    destination = db.query(Destination).filter(
        Destination.id == destination_id
    ).first()
    
    if destination:
        avg_rating = db.query(func.avg(Review.rating)).filter(
            Review.destination_id == destination_id,
            Review.is_approved == True
        ).scalar()
        
        destination.rating = round(avg_rating, 1) if avg_rating else 0.0
        db.commit()
    
    return {
        "message": "Review deleted successfully",
        "success": True
    }


@router.get("/destination/{destination_id}/stats")
async def get_destination_review_stats(
    destination_id: int,
    db: Session = Depends(get_db)
):
    """
    Get review statistics for a destination
    """
    destination = db.query(Destination).filter(
        Destination.id == destination_id
    ).first()
    
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    # Get rating distribution
    total_reviews = db.query(func.count(Review.id)).filter(
        Review.destination_id == destination_id,
        Review.is_approved == True
    ).scalar() or 0
    
    rating_distribution = {}
    for rating in range(1, 6):
        count = db.query(func.count(Review.id)).filter(
            Review.destination_id == destination_id,
            Review.is_approved == True,
            Review.rating == rating
        ).scalar() or 0
        
        rating_distribution[f"{rating}_star"] = count
    
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.destination_id == destination_id,
        Review.is_approved == True
    ).scalar()
    
    return {
        "destination_id": destination_id,
        "destination_name": destination.name,
        "total_reviews": total_reviews,
        "average_rating": round(avg_rating, 1) if avg_rating else 0.0,
        "rating_distribution": rating_distribution
    }