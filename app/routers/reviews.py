from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.auth_service import get_optional_user

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Create a new review"""
    db_review = Review(
        destination_id=review.destination_id,
        user_id=current_user.id if current_user else None,
        user_name=review.user_name or (current_user.username if current_user else None),
        rating=review.rating,
        comment=review.comment,
        is_approved=True  # Auto-approve, can be changed based on requirements
    )
    
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    return db_review

@router.get("/destination/{destination_id}", response_model=List[ReviewResponse])
def get_destination_reviews(
    destination_id: int,
    skip: int = 0,
    limit: int = 100,
    approved_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get reviews for a specific destination"""
    query = db.query(Review).filter(Review.destination_id == destination_id)
    
    if approved_only:
        query = query.filter(Review.is_approved == True)
    
    reviews = query.order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    return reviews

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific review"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review