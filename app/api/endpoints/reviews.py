# app/api/endpoints/reviews.py - Review API Endpoints (WITH PHOTO UPLOAD)
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models.review import Review
from app.models.review_image import ReviewImage
from app.schemas.review import ReviewResponse, ReviewStats
from pathlib import Path
import shutil
import uuid
from datetime import datetime

router = APIRouter()

# Upload directory
UPLOAD_DIR = Path("uploads/reviews")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)


def save_review_image(file: UploadFile) -> str:
    """Save uploaded review image and return path"""
    ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}_{int(datetime.now().timestamp())}.{ext}"
    file_path = UPLOAD_DIR / filename
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    return f"reviews/{filename}"


@router.get("/destination/{destination_id}", response_model=List[ReviewResponse])
def get_destination_reviews(
    destination_id: int,
    is_approved: bool = True,
    db: Session = Depends(get_db)
):
    """Get all reviews for a destination with images"""
    
    reviews = db.query(Review).filter(
        Review.destination_id == destination_id,
        Review.is_approved == is_approved
    ).order_by(Review.created_at.desc()).all()
    
    return reviews


@router.post("/", response_model=ReviewResponse, status_code=201)
async def create_review(
    destination_id: int = Form(...),
    user_name: str = Form(...),
    rating: int = Form(...),
    comment: Optional[str] = Form(None),
    images: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Submit a new review with optional images"""
    
    # Validate destination exists
    from app.models.destination import Destination
    destination = db.query(Destination).filter(
        Destination.id == destination_id
    ).first()
    
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Validate rating
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Create review
    db_review = Review(
        destination_id=destination_id,
        user_name=user_name,
        rating=rating,
        comment=comment,
        is_approved=True
    )
    
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # Handle image uploads (max 5 images)
    if images and images[0].filename:
        for i, image_file in enumerate(images[:5]):  # Limit to 5 images
            if image_file.filename:
                try:
                    image_path = save_review_image(image_file)
                    
                    review_image = ReviewImage(
                        review_id=db_review.id,
                        image_path=image_path
                    )
                    db.add(review_image)
                except Exception as e:
                    print(f"Error saving image {i+1}: {e}")
                    continue
        
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
    ratings_list = [int(r.rating) for r in reviews]
    avg_rating = sum(ratings_list) / total if total > 0 else 0.0
    
    # Count by star
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for rating in ratings_list:
        if rating in rating_counts:
            rating_counts[rating] += 1
    
    return ReviewStats(
        destination_id=destination_id,
        total_reviews=total,
        average_rating=round(avg_rating, 1),
        five_star=rating_counts[5],
        four_star=rating_counts[4],
        three_star=rating_counts[3],
        two_star=rating_counts[2],
        one_star=rating_counts[1]
    )