# app/api/endpoints/reviews.py - Review API Endpoints (FIXED)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewStats

router = APIRouter()


@router.get("/destination/{destination_id}", response_model=List[ReviewResponse])
def get_destination_reviews(
    destination_id: int,
    is_approved: bool = True,
    db: Session = Depends(get_db)
):
    """Get all reviews for a destination"""
    
    reviews = db.query(Review).filter(
        Review.destination_id == destination_id,
        Review.is_approved == is_approved
    ).order_by(Review.created_at.desc()).all()
    
    return reviews


@router.post("/", response_model=ReviewResponse, status_code=201)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """Submit a new review"""
    
    # Create review (will be approved by default for user panel)
    db_review = Review(
        destination_id=review.destination_id,
        user_name=review.user_name,
        rating=review.rating,
        comment=review.comment,
        is_approved=True  # Auto-approve for now
    )
    
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    return db_review


@router.get("/destination/{destination_id}/stats", response_model=ReviewStats)
def get_review_stats(destination_id: int, db: Session = Depends(get_db)):
    """Get review statistics for a destination"""
    
    reviews = db.query(Review).filter(
        Review.destination_id == destination_id,
        Review.is_approved == True
    ).all()
    
    if not reviews:
        return ReviewStats(
            destination_id=destination_id,
            total_reviews=0,
            average_rating=None,
            five_star=0,
            four_star=0,
            three_star=0,
            two_star=0,
            one_star=0
        )
    
    total = len(reviews)
    avg_rating = sum(r.rating for r in reviews) / total
    
    # Count ratings by star level
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in reviews:
        if review.rating in rating_counts:
            rating_counts[review.rating] += 1
    
    return ReviewStats(
        destination_id=destination_id,
        total_reviews=total,
        average_rating=round(avg_rating, 1),  # FIXED: Now avg_rating is a float
        five_star=rating_counts[5],
        four_star=rating_counts[4],
        three_star=rating_counts[3],
        two_star=rating_counts[2],
        one_star=rating_counts[1]
    )