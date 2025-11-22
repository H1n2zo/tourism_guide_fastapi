"""
Category API Endpoints
CRUD operations for categories
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from models.category import Category
from models.destination import Destination
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from core.security import get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """
    Get all categories
    """
    categories = db.query(Category).order_by(Category.name).all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get single category by ID
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create new category (Admin only)
    """
    # Check if category name already exists
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update category (Admin only)
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if new name conflicts with existing category
    if category.name != db_category.name:
        existing = db.query(Category).filter(
            Category.name == category.name,
            Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
    
    # Update fields
    for field, value in category.dict(exclude_unset=True).items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete category (Admin only)
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if category has destinations
    destination_count = db.query(Destination).filter(
        Destination.category_id == category_id
    ).count()
    
    if destination_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {destination_count} destinations. Please reassign or delete destinations first."
        )
    
    db.delete(category)
    db.commit()
    
    return {
        "message": "Category deleted successfully",
        "success": True
    }


@router.get("/{category_id}/destinations")
async def get_category_destinations(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all destinations in a category
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    destinations = db.query(Destination)\
        .filter(Destination.category_id == category_id)\
        .order_by(Destination.name)\
        .all()
    
    return {
        "category": category,
        "destinations": destinations,
        "count": len(destinations)
    }