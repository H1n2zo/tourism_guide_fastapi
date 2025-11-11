# app/api/endpoints/categories.py - Category API Endpoints (FIXED)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.category import Category
from app.models.destination import Destination
from app.schemas.category import CategoryResponse

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Get all categories with destination count"""
    
    categories = db.query(
        Category,
        func.count(Destination.id).label('destination_count')
    ).outerjoin(
        Destination, Category.id == Destination.category_id
    ).group_by(
        Category.id
    ).order_by(
        Category.name
    ).all()
    
    result = []
    for category, dest_count in categories:
        cat_data = {
            **category.__dict__,
            'destination_count': dest_count
        }
        result.append(CategoryResponse(**cat_data))
    
    return result


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get single category by ID"""
    
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    dest_count = db.query(func.count(Destination.id)).filter(
        Destination.category_id == category_id
    ).scalar()
    
    cat_data = {
        **category.__dict__,
        'destination_count': dest_count or 0
    }
    
    return CategoryResponse(**cat_data)