# destination.py
"""
Destination Details Page with Reviews
Converted from destination.php
"""

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from config.database import (
    get_db, Destination, Category, DestinationImage, 
    Review, UPLOAD_URL
)
from auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/destination/{destination_id}", response_class=HTMLResponse)
async def destination_details(
    destination_id: int,
    request: Request,
    success: str = None,
    db: Session = Depends(get_db)
):
    """Display destination details with reviews"""
    
    # Get current user
    current_user = get_current_user(request, db)
    
    # Fetch destination with category
    destination_query = db.query(
        Destination,
        Category.name.label('category_name'),
        Category.icon.label('icon')
    ).outerjoin(
        Category, Destination.category_id == Category.id
    ).filter(
        Destination.id == destination_id
    ).first()
    
    if not destination_query:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    dest, category_name, icon = destination_query
    
    # Fetch additional images
    images = db.query(DestinationImage).filter(
        DestinationImage.destination_id == destination_id
    ).order_by(DestinationImage.is_primary.desc()).all()
    
    # Fetch approved reviews
    reviews = db.query(Review).filter(
        Review.destination_id == destination_id,
        Review.is_approved == True
    ).order_by(Review.created_at.desc()).all()
    
    # Calculate rating statistics
    rating_stats = db.query(
        func.count(Review.id).label('count'),
        func.avg(Review.rating).label('avg_rating')
    ).filter(
        Review.destination_id == destination_id,
        Review.is_approved == True
    ).first()
    
    # Format destination data
    destination_data = {
        'id': dest.id,
        'name': dest.name,
        'category_name': category_name,
        'icon': icon,
        'description': dest.description,
        'address': dest.address,
        'latitude': float(dest.latitude) if dest.latitude else None,
        'longitude': float(dest.longitude) if dest.longitude else None,
        'contact_number': dest.contact_number,
        'email': dest.email,
        'website': dest.website,
        'opening_hours': dest.opening_hours,
        'entry_fee': dest.entry_fee,
        'image_path': dest.image_path
    }
    
    return templates.TemplateResponse("destination.html", {
        "request": request,
        "destination": destination_data,
        "images": images,
        "reviews": reviews,
        "rating_count": rating_stats.count if rating_stats else 0,
        "avg_rating": float(rating_stats.avg_rating) if rating_stats and rating_stats.avg_rating else 0,
        "success": success,
        "current_user": current_user,
        "UPLOAD_URL": UPLOAD_URL
    })


@router.post("/destination/{destination_id}/review")
async def submit_review(
    destination_id: int,
    request: Request,
    review_name: str = Form(...),
    rating: int = Form(..., ge=1, le=5),
    comment: str = Form(...),
    db: Session = Depends(get_db)
):
    """Submit a review for a destination"""
    
    # Get current user (if logged in)
    current_user = get_current_user(request, db)
    user_id = current_user.id if current_user else None
    
    # Validate rating
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Create review
    new_review = Review(
        destination_id=destination_id,
        user_id=user_id,
        user_name=review_name,
        rating=rating,
        comment=comment,
        is_approved=True  # Auto-approve for now
    )
    
    db.add(new_review)
    db.commit()
    
    # Redirect back with success message
    return RedirectResponse(
        url=f"/destination/{destination_id}?success=1",
        status_code=303
    )