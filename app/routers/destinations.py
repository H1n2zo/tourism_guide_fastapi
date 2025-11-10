from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from app.database import get_db
from app.models.destination import Destination, Category
from app.models.review import Review
from app.schemas.destination import (
    DestinationResponse,
    DestinationListResponse,
    CategoryResponse
)

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    """Get all categories"""
    categories = db.query(Category).order_by(Category.name).all()
    return categories

@router.get("/", response_model=List[DestinationListResponse])
def get_destinations(
    search: Optional[str] = Query(None, description="Search by name or description"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    is_active: bool = Query(True, description="Filter by active status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all destinations with optional filters"""
    query = db.query(
        Destination,
        Category.name.label('category_name'),
        Category.icon.label('category_icon'),
        func.count(Review.id).label('review_count'),
        func.round(func.avg(Review.rating), 1).label('avg_rating')
    ).outerjoin(
        Category, Destination.category_id == Category.id
    ).outerjoin(
        Review, (Destination.id == Review.destination_id) & (Review.is_approved == True)
    ).filter(
        Destination.is_active == is_active
    )
    
    # Apply filters
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Destination.name.like(search_pattern)) |
            (Destination.description.like(search_pattern))
        )
    
    if category_id:
        query = query.filter(Destination.category_id == category_id)
    
    query = query.group_by(Destination.id).order_by(Destination.name)
    
    destinations = query.offset(skip).limit(limit).all()
    
    # Format response
    result = []
    for dest, cat_name, cat_icon, review_count, avg_rating in destinations:
        result.append({
            "id": dest.id,
            "name": dest.name,
            "category_id": dest.category_id,
            "description": dest.description,
            "latitude": dest.latitude,
            "longitude": dest.longitude,
            "rating": dest.rating,
            "image_path": dest.image_path,
            "is_active": dest.is_active,
            "category_name": cat_name,
            "category_icon": cat_icon,
            "review_count": review_count or 0,
            "avg_rating": float(avg_rating) if avg_rating else 0.0
        })
    
    return result

@router.get("/{destination_id}", response_model=DestinationResponse)
def get_destination(
    destination_id: int,
    db: Session = Depends(get_db)
):
    """Get destination by ID with images and ratings"""
    # Get destination with review stats
    result = db.query(
        Destination,
        func.count(Review.id).label('review_count'),
        func.round(func.avg(Review.rating), 1).label('avg_rating')
    ).outerjoin(
        Review, (Destination.id == Review.destination_id) & (Review.is_approved == True)
    ).filter(
        Destination.id == destination_id
    ).group_by(Destination.id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    destination, review_count, avg_rating = result
    
    # Add review stats to response
    dest_dict = {
        **destination.__dict__,
        "review_count": review_count or 0,
        "avg_rating": float(avg_rating) if avg_rating else 0.0
    }
    
    return dest_dict

@router.get("/statistics/summary")
def get_statistics(db: Session = Depends(get_db)):
    """Get overall statistics"""
    total_destinations = db.query(func.count(Destination.id)).filter(
        Destination.is_active == True
    ).scalar()
    
    total_reviews = db.query(func.count(Review.id)).filter(
        Review.is_approved == True
    ).scalar()
    
    total_categories = db.query(func.count(Category.id)).scalar()
    
    return {
        "total_destinations": total_destinations or 0,
        "total_reviews": total_reviews or 0,
        "total_categories": total_categories or 0
    }