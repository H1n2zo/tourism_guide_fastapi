# app/api/endpoints/admin.py - Admin Panel API Routes (FIXED)
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List
from decimal import Decimal

from app.database import get_db
from app.api.deps import require_admin
from app.models.user import User, UserRole
from app.models.destination import Destination, DestinationImage
from app.models.category import Category
from app.models.route import Route, TransportMode
from app.models.review import Review
from app.models.feedback import WebsiteFeedback
from app.schemas.destination import DestinationResponse
from app.schemas.category import CategoryResponse
from app.schemas.route import RouteResponse
import os
import shutil
from pathlib import Path
import uuid
from datetime import datetime

router = APIRouter()

# File upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
(UPLOAD_DIR / "destinations").mkdir(exist_ok=True)
(UPLOAD_DIR / "categories").mkdir(exist_ok=True)


# ============ DASHBOARD ============
@router.get("/dashboard/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get dashboard statistics"""
    
    total_destinations = db.query(func.count(Destination.id)).scalar() or 0
    active_destinations = db.query(func.count(Destination.id)).filter(
        Destination.is_active == True
    ).scalar() or 0
    total_categories = db.query(func.count(Category.id)).scalar() or 0
    total_routes = db.query(func.count(Route.id)).scalar() or 0
    total_reviews = db.query(func.count(Review.id)).scalar() or 0
    pending_reviews = db.query(func.count(Review.id)).filter(
        Review.is_approved == False
    ).scalar() or 0
    total_feedback = db.query(func.count(WebsiteFeedback.id)).scalar() or 0
    unread_feedback = db.query(func.count(WebsiteFeedback.id)).filter(
        WebsiteFeedback.is_read == False
    ).scalar() or 0
    
    # Recent destinations
    recent_destinations = db.query(Destination).order_by(
        Destination.created_at.desc()
    ).limit(5).all()
    
    return {
        "total_destinations": total_destinations,
        "active_destinations": active_destinations,
        "total_categories": total_categories,
        "total_routes": total_routes,
        "total_reviews": total_reviews,
        "pending_reviews": pending_reviews,
        "total_feedback": total_feedback,
        "unread_feedback": unread_feedback,
        "recent_destinations": [
            {
                "id": d.id,
                "name": d.name,
                "is_active": d.is_active,
                "created_at": d.created_at
            } for d in recent_destinations
        ]
    }


# ============ DESTINATIONS MANAGEMENT ============
@router.post("/destinations")
async def create_destination(
    name: str = Form(...),
    category_id: int = Form(...),
    description: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    contact_number: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    opening_hours: Optional[str] = Form(None),
    entry_fee: Optional[str] = Form(None),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new destination"""
    
    # Handle image upload
    image_path = None
    if image and image.filename:
        # Extract extension safely
        filename_parts = image.filename.split('.')
        ext = filename_parts[-1] if len(filename_parts) > 1 else 'jpg'
        filename = f"{uuid.uuid4()}_{int(datetime.now().timestamp())}.{ext}"
        file_path = UPLOAD_DIR / "destinations" / filename
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        
        image_path = f"destinations/{filename}"
    
    # Create destination - proper attribute assignment
    new_dest = Destination(
        name=name,
        category_id=category_id,
        description=description,
        address=address,
        latitude=Decimal(str(latitude)) if latitude is not None else None,
        longitude=Decimal(str(longitude)) if longitude is not None else None,
        contact_number=contact_number,
        email=email,
        website=website,
        opening_hours=opening_hours,
        entry_fee=entry_fee,
        image_path=image_path,
        is_active=is_active
    )
    
    db.add(new_dest)
    db.commit()
    db.refresh(new_dest)
    
    return {"message": "Destination created successfully", "id": new_dest.id}


@router.put("/destinations/{destination_id}")
async def update_destination(
    destination_id: int,
    name: str = Form(...),
    category_id: int = Form(...),
    description: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    contact_number: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    opening_hours: Optional[str] = Form(None),
    entry_fee: Optional[str] = Form(None),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update destination"""
    
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Handle image upload
    if image and image.filename:
        # Delete old image
        old_image_path = str(dest.image_path) if dest.image_path else None
        if old_image_path:
            old_path = UPLOAD_DIR / old_image_path
            if old_path.exists():
                old_path.unlink()
        
        # Upload new image
        filename_parts = image.filename.split('.')
        ext = filename_parts[-1] if len(filename_parts) > 1 else 'jpg'
        filename = f"{uuid.uuid4()}_{int(datetime.now().timestamp())}.{ext}"
        file_path = UPLOAD_DIR / "destinations" / filename
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        
        dest.image_path = f"destinations/{filename}"
    
    # Update fields properly using setattr or direct assignment
    dest.name = name
    dest.category_id = category_id
    dest.description = description
    dest.address = address
    dest.latitude = Decimal(str(latitude)) if latitude is not None else None
    dest.longitude = Decimal(str(longitude)) if longitude is not None else None
    dest.contact_number = contact_number
    dest.email = email
    dest.website = website
    dest.opening_hours = opening_hours
    dest.entry_fee = entry_fee
    dest.is_active = is_active
    
    db.commit()
    
    return {"message": "Destination updated successfully"}


@router.delete("/destinations/{destination_id}")
async def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete destination"""
    
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Delete image
    image_path_str = str(dest.image_path) if dest.image_path else None
    if image_path_str:
        image_path = UPLOAD_DIR / image_path_str
        if image_path.exists():
            image_path.unlink()
    
    db.delete(dest)
    db.commit()
    
    return {"message": "Destination deleted successfully"}


@router.patch("/destinations/{destination_id}/toggle")
async def toggle_destination_status(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Toggle destination active status"""
    
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # FIX: Properly toggle boolean
    current_status = bool(dest.is_active)
    dest.is_active = not current_status
    db.commit()
    
    return {"message": "Status updated", "is_active": dest.is_active}


# ============ CATEGORIES MANAGEMENT ============
@router.post("/categories")
async def create_category(
    name: str = Form(...),
    icon: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new category"""
    
    new_cat = Category(name=name, icon=icon)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    
    return {"message": "Category created successfully", "id": new_cat.id}


@router.put("/categories/{category_id}")
async def update_category(
    category_id: int,
    name: str = Form(...),
    icon: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update category"""
    
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    
    cat.name = name
    cat.icon = icon
    db.commit()
    
    return {"message": "Category updated successfully"}


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete category"""
    
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has destinations
    dest_count = db.query(func.count(Destination.id)).filter(
        Destination.category_id == category_id
    ).scalar()
    
    if dest_count and dest_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category with {dest_count} destinations"
        )
    
    db.delete(cat)
    db.commit()
    
    return {"message": "Category deleted successfully"}


# ============ ROUTES MANAGEMENT ============
@router.post("/routes")
async def create_route(
    route_name: Optional[str] = Form(None),
    origin_id: int = Form(...),
    destination_id: int = Form(...),
    transport_mode: str = Form(...),
    distance_km: Optional[float] = Form(None),
    estimated_time_minutes: Optional[int] = Form(None),
    base_fare: Optional[float] = Form(None),
    fare_per_km: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    is_active: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new route"""
    
    new_route = Route(
        route_name=route_name,
        origin_id=origin_id,
        destination_id=destination_id,
        transport_mode=TransportMode(transport_mode),
        distance_km=Decimal(str(distance_km)) if distance_km is not None else None,
        estimated_time_minutes=estimated_time_minutes,
        base_fare=Decimal(str(base_fare)) if base_fare is not None else None,
        fare_per_km=Decimal(str(fare_per_km)) if fare_per_km is not None else None,
        description=description,
        is_active=is_active
    )
    
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    
    return {"message": "Route created successfully", "id": new_route.id}


@router.delete("/routes/{route_id}")
async def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete route"""
    
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    db.delete(route)
    db.commit()
    
    return {"message": "Route deleted successfully"}


# ============ REVIEWS MANAGEMENT ============
@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete review"""
    
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    
    return {"message": "Review deleted successfully"}


@router.patch("/reviews/{review_id}/toggle")
async def toggle_review_approval(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Toggle review approval"""
    
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # FIX: Properly toggle boolean
    current_status = bool(review.is_approved)
    review.is_approved = not current_status
    db.commit()
    
    return {"message": "Review status updated", "is_approved": review.is_approved}


# ============ FEEDBACK MANAGEMENT ============
@router.get("/feedback")
async def get_all_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all feedback"""
    
    feedbacks = db.query(WebsiteFeedback).order_by(
        WebsiteFeedback.is_read.asc(),
        WebsiteFeedback.created_at.desc()
    ).all()
    
    return feedbacks


@router.patch("/feedback/{feedback_id}/read")
async def mark_feedback_read(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
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
async def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
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


# ============ USERS MANAGEMENT ============
@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all users"""
    
    users = db.query(User).order_by(User.created_at.desc()).all()
    
    return [{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role.value,
        "created_at": u.created_at
    } for u in users]


@router.patch("/users/{user_id}/toggle-role")
async def toggle_user_role(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Toggle user role between admin and user"""
    
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400, 
            detail="Cannot change your own role"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # FIX: Properly toggle role
    current_role = user.role
    new_role = UserRole.USER if current_role == UserRole.ADMIN else UserRole.ADMIN
    user.role = new_role
    db.commit()
    
    return {"message": "User role updated", "role": user.role.value}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete user"""
    
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete your own account"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}