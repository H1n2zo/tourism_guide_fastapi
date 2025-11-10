from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.destination import Destination, Category, DestinationImage
from app.models.review import Review, WebsiteFeedback
from app.models.route import Route
from app.dependencies import get_current_admin
from app.services.file_service import save_upload_file, delete_upload_file
from decimal import Decimal

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# Dashboard Statistics
@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get dashboard statistics"""
    total_destinations = db.query(func.count(Destination.id)).scalar()
    active_destinations = db.query(func.count(Destination.id)).filter(
        Destination.is_active == True
    ).scalar()
    total_categories = db.query(func.count(Category.id)).scalar()
    total_routes = db.query(func.count(Route.id)).scalar()
    total_reviews = db.query(func.count(Review.id)).scalar()
    unread_feedback = db.query(func.count(WebsiteFeedback.id)).filter(
        WebsiteFeedback.is_read == False
    ).scalar()
    
    return {
        "total_destinations": total_destinations or 0,
        "active_destinations": active_destinations or 0,
        "total_categories": total_categories or 0,
        "total_routes": total_routes or 0,
        "total_reviews": total_reviews or 0,
        "unread_feedback": unread_feedback or 0
    }

# Destination Management
@router.post("/destinations")
async def create_destination(
    name: str = Form(...),
    category_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    contact_number: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    opening_hours: Optional[str] = Form(None),
    entry_fee: Optional[str] = Form(None),
    rating: Optional[float] = Form(0.0),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create new destination"""
    image_path = None
    if image:
        image_path = save_upload_file(image, "destinations")
    
    destination = Destination(
        name=name,
        category_id=category_id,
        description=description,
        address=address,
        latitude=Decimal(str(latitude)) if latitude else None,
        longitude=Decimal(str(longitude)) if longitude else None,
        contact_number=contact_number,
        email=email,
        website=website,
        opening_hours=opening_hours,
        entry_fee=entry_fee,
        rating=Decimal(str(rating)),
        image_path=image_path,
        is_active=is_active
    )
    
    db.add(destination)
    db.commit()
    db.refresh(destination)
    
    return {"id": destination.id, "message": "Destination created successfully"}

@router.put("/destinations/{destination_id}")
async def update_destination(
    destination_id: int,
    name: str = Form(...),
    category_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    contact_number: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    opening_hours: Optional[str] = Form(None),
    entry_fee: Optional[str] = Form(None),
    rating: Optional[float] = Form(0.0),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update destination"""
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Handle image update
    if image:
        if destination.image_path:
            delete_upload_file(destination.image_path)
        destination.image_path = save_upload_file(image, "destinations")
    
    # Update fields
    destination.name = name
    destination.category_id = category_id
    destination.description = description
    destination.address = address
    destination.latitude = Decimal(str(latitude)) if latitude else None
    destination.longitude = Decimal(str(longitude)) if longitude else None
    destination.contact_number = contact_number
    destination.email = email
    destination.website = website
    destination.opening_hours = opening_hours
    destination.entry_fee = entry_fee
    destination.rating = Decimal(str(rating))
    destination.is_active = is_active
    
    db.commit()
    db.refresh(destination)
    
    return {"message": "Destination updated successfully"}

@router.delete("/destinations/{destination_id}")
def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete destination"""
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Delete image
    if destination.image_path:
        delete_upload_file(destination.image_path)
    
    # Delete additional images
    images = db.query(DestinationImage).filter(
        DestinationImage.destination_id == destination_id
    ).all()
    for img in images:
        delete_upload_file(img.image_path)
    
    db.delete(destination)
    db.commit()
    
    return {"message": "Destination deleted successfully"}

# Category Management
@router.post("/categories")
def create_category(
    name: str = Form(...),
    icon: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create new category"""
    category = Category(name=name, icon=icon)
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return {"id": category.id, "message": "Category created successfully"}

@router.put("/categories/{category_id}")
def update_category(
    category_id: int,
    name: str = Form(...),
    icon: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.name = name
    category.icon = icon
    
    db.commit()
    return {"message": "Category updated successfully"}

@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has destinations
    dest_count = db.query(func.count(Destination.id)).filter(
        Destination.category_id == category_id
    ).scalar()
    
    if dest_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete category with {dest_count} destinations"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}

# Route Management
@router.post("/routes")
def create_route(
    route_name: Optional[str] = Form(None),
    origin_id: Optional[int] = Form(None),
    destination_id: Optional[int] = Form(None),
    transport_mode: str = Form(...),
    distance_km: Optional[float] = Form(None),
    estimated_time_minutes: Optional[int] = Form(None),
    base_fare: Optional[float] = Form(None),
    fare_per_km: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    is_active: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create new route"""
    route = Route(
        route_name=route_name,
        origin_id=origin_id,
        destination_id=destination_id,
        transport_mode=transport_mode,
        distance_km=Decimal(str(distance_km)) if distance_km else None,
        estimated_time_minutes=estimated_time_minutes,
        base_fare=Decimal(str(base_fare)) if base_fare else None,
        fare_per_km=Decimal(str(fare_per_km)) if fare_per_km else None,
        description=description,
        is_active=is_active
    )
    
    db.add(route)
    db.commit()
    db.refresh(route)
    
    return {"id": route.id, "message": "Route created successfully"}

@router.delete("/routes/{route_id}")
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete route"""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    db.delete(route)
    db.commit()
    
    return {"message": "Route deleted successfully"}

# Review Management
@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete review"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    
    return {"message": "Review deleted successfully"}

@router.put("/reviews/{review_id}/toggle")
def toggle_review_approval(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Toggle review approval status"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.is_approved = not review.is_approved
    db.commit()
    
    return {"message": "Review status updated", "is_approved": review.is_approved}

# Feedback Management
@router.get("/feedback")
def get_all_feedback(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get all feedback"""
    feedbacks = db.query(WebsiteFeedback).order_by(
        WebsiteFeedback.is_read.asc(),
        WebsiteFeedback.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return feedbacks

@router.put("/feedback/{feedback_id}/read")
def mark_feedback_read(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Mark feedback as read"""
    feedback = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.is_read = True
    db.commit()
    
    return {"message": "Feedback marked as read"}

@router.delete("/feedback/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete feedback"""
    feedback = db.query(WebsiteFeedback).filter(
        WebsiteFeedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    db.delete(feedback)
    db.commit()
    
    return {"message": "Feedback deleted successfully"}