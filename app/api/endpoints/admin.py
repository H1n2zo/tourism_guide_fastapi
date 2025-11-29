# app/api/endpoints/admin.py - FIXED: Add Multiple Photos Support
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List
from decimal import Decimal

from app.database import get_db
from app.api.deps import require_admin
from app.models.user import User
from app.models.destination import Destination, DestinationImage
from app.models.category import Category
from app.models.route import Route, TransportMode
from app.models.review import Review
from app.models.feedback import WebsiteFeedback
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


# ============ HELPER FUNCTIONS ============
def save_uploaded_file(file: UploadFile, folder: str) -> str:
    """Save uploaded file and return path"""
    ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}_{int(datetime.now().timestamp())}.{ext}"
    file_path = UPLOAD_DIR / folder / filename
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    return f"{folder}/{filename}"


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
    additional_photos: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new destination with multiple photos"""
    
    # Handle featured image upload
    image_path = None
    if image:
        image_path = save_uploaded_file(image, "destinations")
    
    # Create destination
    new_dest = Destination(
        name=name,
        category_id=category_id,
        description=description,
        address=address,
        latitude=latitude,
        longitude=longitude,
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
    
    # Handle additional photos
    if additional_photos and additional_photos[0].filename:
        for photo_file in additional_photos:
            if photo_file.filename:
                photo_path = save_uploaded_file(photo_file, "destinations")
                
                new_image = DestinationImage(
                    destination_id=new_dest.id,
                    image_path=photo_path,
                    caption=""
                )
                db.add(new_image)
        
        db.commit()
    
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
    additional_photos: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update destination with multiple photos"""
    
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Handle featured image upload
    if image and image.filename:
        # Delete old image
        if dest.image_path:
            old_path = UPLOAD_DIR / dest.image_path
            if old_path.exists():
                old_path.unlink()
        
        dest.image_path = save_uploaded_file(image, "destinations")
    
    # Update fields
    dest.name = name
    dest.category_id = category_id
    dest.description = description
    dest.address = address
    dest.latitude = latitude
    dest.longitude = longitude
    dest.contact_number = contact_number
    dest.email = email
    dest.website = website
    dest.opening_hours = opening_hours
    dest.entry_fee = entry_fee
    dest.is_active = is_active
    
    db.commit()
    
    # Handle additional photos
    if additional_photos and additional_photos[0].filename:
        for photo_file in additional_photos:
            if photo_file.filename:
                photo_path = save_uploaded_file(photo_file, "destinations")
                
                new_image = DestinationImage(
                    destination_id=destination_id,
                    image_path=photo_path,
                    caption=""
                )
                db.add(new_image)
        
        db.commit()
    
    return {"message": "Destination updated successfully"}


@router.delete("/destination-images/{image_id}")
async def delete_destination_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a destination gallery image"""
    
    image = db.query(DestinationImage).filter(DestinationImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Delete file
    image_path = UPLOAD_DIR / image.image_path
    if image_path.exists():
        image_path.unlink()
    
    db.delete(image)
    db.commit()
    
    return {"message": "Image deleted successfully"}


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
    
    # Delete featured image
    if dest.image_path:
        image_path = UPLOAD_DIR / dest.image_path
        if image_path.exists():
            image_path.unlink()
    
    # Delete gallery images (cascade will handle DB, but we need to delete files)
    gallery_images = db.query(DestinationImage).filter(
        DestinationImage.destination_id == destination_id
    ).all()
    
    for img in gallery_images:
        img_path = UPLOAD_DIR / img.image_path
        if img_path.exists():
            img_path.unlink()
    
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
    
    dest.is_active = not dest.is_active
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
    
    if dest_count > 0:
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
        transport_mode=transport_mode,
        distance_km=distance_km,
        estimated_time_minutes=estimated_time_minutes,
        base_fare=base_fare,
        fare_per_km=fare_per_km,
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
    
    review.is_approved = not review.is_approved
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
    
    from app.models.user import UserRole
    user.role = UserRole.USER if user.role == UserRole.ADMIN else UserRole.ADMIN
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