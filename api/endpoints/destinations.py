"""
Destination API Endpoints
CRUD operations for destinations
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
import os
import shutil
from datetime import datetime

from config.database import get_db
from config.settings import settings
from models.destination import Destination
from models.category import Category
from models.review import Review
from models.destination_image import DestinationImage
from schemas.destination import (
    DestinationCreate,
    DestinationUpdate,
    DestinationResponse,
    PaginationParams
)
from core.security import get_current_admin_user
from core.utils import save_upload_file, delete_upload_file

router = APIRouter()


@router.get("/", response_model=List[DestinationResponse])
async def get_destinations(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get all destinations with optional filtering and pagination
    """
    query = db.query(
        Destination,
        Category.name.label('category_name'),
        Category.icon.label('category_icon'),
        func.count(Review.id).label('review_count'),
        func.avg(Review.rating).label('avg_rating')
    ).outerjoin(Category).outerjoin(Review)
    
    # Filters
    if search:
        query = query.filter(
            or_(
                Destination.name.contains(search),
                Destination.description.contains(search)
            )
        )
    
    if category_id:
        query = query.filter(Destination.category_id == category_id)
    
    if is_active is not None:
        query = query.filter(Destination.is_active == is_active)
    
    # Group by and order
    query = query.group_by(Destination.id).order_by(Destination.name)
    
    # Pagination
    offset = (page - 1) * page_size
    results = query.offset(offset).limit(page_size).all()
    
    # Format response
    destinations = []
    for dest, cat_name, cat_icon, review_count, avg_rating in results:
        dest_dict = {
            **dest.__dict__,
            'category_name': cat_name,
            'category_icon': cat_icon,
            'review_count': review_count or 0,
            'avg_rating': float(avg_rating) if avg_rating else None
        }
        destinations.append(dest_dict)
    
    return destinations


@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(destination_id: int, db: Session = Depends(get_db)):
    """
    Get single destination by ID with full details
    """
    result = db.query(
        Destination,
        Category.name.label('category_name'),
        Category.icon.label('category_icon'),
        func.count(Review.id).label('review_count'),
        func.avg(Review.rating).label('avg_rating')
    ).outerjoin(Category).outerjoin(Review)\
     .filter(Destination.id == destination_id)\
     .group_by(Destination.id)\
     .first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    dest, cat_name, cat_icon, review_count, avg_rating = result
    
    return {
        **dest.__dict__,
        'category_name': cat_name,
        'category_icon': cat_icon,
        'review_count': review_count or 0,
        'avg_rating': float(avg_rating) if avg_rating else None
    }


@router.post("/", response_model=DestinationResponse, status_code=status.HTTP_201_CREATED)
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
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create new destination (Admin only)
    """
    # Handle image upload
    image_path = None
    if image:
        image_path = await save_upload_file(image, "destinations")
    
    # Create destination
    new_destination = Destination(
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
    
    db.add(new_destination)
    db.commit()
    db.refresh(new_destination)
    
    return new_destination


@router.put("/{destination_id}", response_model=DestinationResponse)
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
    is_active: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update destination (Admin only)
    """
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    # Handle new image upload
    if image:
        # Delete old image
        if destination.image_path:
            delete_upload_file(destination.image_path)
        
        # Save new image
        destination.image_path = await save_upload_file(image, "destinations")
    
    # Update fields
    destination.name = name
    destination.category_id = category_id
    destination.description = description
    destination.address = address
    destination.latitude = latitude
    destination.longitude = longitude
    destination.contact_number = contact_number
    destination.email = email
    destination.website = website
    destination.opening_hours = opening_hours
    destination.entry_fee = entry_fee
    if is_active is not None:
        destination.is_active = is_active
    
    db.commit()
    db.refresh(destination)
    
    return destination


@router.delete("/{destination_id}")
async def delete_destination(
    destination_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete destination (Admin only)
    """
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    # Delete image file
    if destination.image_path:
        delete_upload_file(destination.image_path)
    
    # Delete all associated images
    for img in destination.images:
        delete_upload_file(img.image_path)
    
    db.delete(destination)
    db.commit()
    
    return {
        "message": "Destination deleted successfully",
        "success": True
    }


@router.post("/{destination_id}/images")
async def add_destination_image(
    destination_id: int,
    image: UploadFile = File(...),
    caption: Optional[str] = Form(None),
    is_primary: bool = Form(False),
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Add additional image to destination (Admin only)
    """
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    # Save image
    image_path = await save_upload_file(image, "destinations")
    
    # Create image record
    new_image = DestinationImage(
        destination_id=destination_id,
        image_path=image_path,
        caption=caption,
        is_primary=is_primary
    )
    
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    
    return {
        "message": "Image added successfully",
        "image": new_image,
        "success": True
    }


@router.delete("/images/{image_id}")
async def delete_destination_image(
    image_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete destination image (Admin only)
    """
    image = db.query(DestinationImage).filter(DestinationImage.id == image_id).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Delete file
    delete_upload_file(image.image_path)
    
    db.delete(image)
    db.commit()
    
    return {
        "message": "Image deleted successfully",
        "success": True
    }


@router.get("/search/autocomplete")
async def autocomplete_destinations(
    q: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Autocomplete search for destinations
    """
    destinations = db.query(Destination.id, Destination.name)\
        .filter(
            Destination.is_active == True,
            Destination.name.contains(q)
        )\
        .limit(limit)\
        .all()
    
    return [{"id": d.id, "name": d.name} for d in destinations]