# app/api/endpoints/destinations.py - Destination API Endpoints (FIXED)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional
from app.database import get_db
from app.models.destination import Destination, DestinationImage
from app.models.category import Category
from app.models.review import Review
from app.schemas.destination import DestinationResponse, DestinationListResponse

router = APIRouter()


# app/api/endpoints/destinations.py - FIXED to allow fetching inactive items

@router.get("/", response_model=DestinationListResponse)
def get_destinations(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    is_active: Optional[bool] = None,  # ✅ Make it optional (None = all)
    db: Session = Depends(get_db)
):
    """Get list of destinations with pagination and filters"""
    
    # Base query - NO default filter on is_active
    query = db.query(Destination)
    
    # ✅ Only filter by is_active if explicitly provided
    if is_active is not None:
        query = query.filter(Destination.is_active == is_active)
    
    # Apply other filters
    if search:
        query = query.filter(
            or_(
                Destination.name.ilike(f"%{search}%"),
                Destination.description.ilike(f"%{search}%")
            )
        )
    
    if category_id:
        query = query.filter(Destination.category_id == category_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    destinations = query.order_by(Destination.name).offset(offset).limit(page_size).all()
    
    # Enrich with category and review data
    result_destinations = []
    for dest in destinations:
        # Get category info
        category = db.query(Category).filter(Category.id == dest.category_id).first()
        
        # Get review statistics
        review_stats = db.query(
            func.count(Review.id).label('count'),
            func.avg(Review.rating).label('avg_rating')
        ).filter(
            Review.destination_id == dest.id,
            Review.is_approved == True
        ).first()
        
        # Safely extract values
        review_count = int(review_stats[0]) if review_stats and review_stats[0] else 0
        avg_rating = float(review_stats[1]) if review_stats and review_stats[1] else None
        
        # Build response
        dest_data = {
            **dest.__dict__,
            'category_name': category.name if category else None,
            'category_icon': category.icon if category else None,
            'review_count': review_count,
            'avg_rating': avg_rating
        }
        result_destinations.append(DestinationResponse(**dest_data))
    
    total_pages = (total + page_size - 1) // page_size
    
    return DestinationListResponse(
        destinations=result_destinations,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{destination_id}", response_model=DestinationResponse)
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    """Get single destination by ID with all related data"""
    
    destination = db.query(Destination).filter(
        Destination.id == destination_id,
        Destination.is_active == True
    ).first()
    
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Get category info
    category = db.query(Category).filter(Category.id == destination.category_id).first()
    
    # Get images
    images = db.query(DestinationImage).filter(
        DestinationImage.destination_id == destination_id
    ).all()
    
    # Get review statistics
    review_stats = db.query(
        func.count(Review.id).label('count'),
        func.avg(Review.rating).label('avg_rating')
    ).filter(
        Review.destination_id == destination_id,
        Review.is_approved == True
    ).first()
    
    # Safely extract values
    review_count = int(review_stats[0]) if review_stats and review_stats[0] else 0
    avg_rating = float(review_stats[1]) if review_stats and review_stats[1] else None
    
    # Build response
    dest_data = {
        **destination.__dict__,
        'category_name': category.name if category else None,
        'category_icon': category.icon if category else None,
        'images': images,
        'review_count': review_count,
        'avg_rating': avg_rating
    }
    
    return DestinationResponse(**dest_data)


@router.get("/stats/summary")
def get_destination_stats(db: Session = Depends(get_db)):
    """Get destination statistics for homepage"""
    
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