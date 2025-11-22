"""
Admin API Endpoints
Dashboard statistics and admin-only operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from config.database import get_db
from models.user import User
from models.destination import Destination
from models.category import Category
from models.review import Review
from models.route import Route
from models.feedback import WebsiteFeedback
from schemas.user import UserResponse
from core.security import get_current_admin_user, get_password_hash

router = APIRouter()


@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics (Admin only)
    """
    # Count totals
    total_destinations = db.query(func.count(Destination.id)).scalar() or 0
    active_destinations = db.query(func.count(Destination.id))\
        .filter(Destination.is_active == True).scalar() or 0
    
    total_categories = db.query(func.count(Category.id)).scalar() or 0
    total_reviews = db.query(func.count(Review.id)).scalar() or 0
    approved_reviews = db.query(func.count(Review.id))\
        .filter(Review.is_approved == True).scalar() or 0
    pending_reviews = db.query(func.count(Review.id))\
        .filter(Review.is_approved == False).scalar() or 0
    
    total_routes = db.query(func.count(Route.id)).scalar() or 0
    active_routes = db.query(func.count(Route.id))\
        .filter(Route.is_active == True).scalar() or 0
    
    total_users = db.query(func.count(User.id)).scalar() or 0
    admin_users = db.query(func.count(User.id))\
        .filter(User.role == 'admin').scalar() or 0
    
    total_feedback = db.query(func.count(WebsiteFeedback.id)).scalar() or 0
    unread_feedback = db.query(func.count(WebsiteFeedback.id))\
        .filter(WebsiteFeedback.is_read == False).scalar() or 0
    
    # Average ratings
    avg_destination_rating = db.query(func.avg(Destination.rating)).scalar()
    avg_website_rating = db.query(func.avg(WebsiteFeedback.rating)).scalar()
    
    return {
        "destinations": {
            "total": total_destinations,
            "active": active_destinations,
            "inactive": total_destinations - active_destinations,
            "avg_rating": round(avg_destination_rating, 1) if avg_destination_rating else 0.0
        },
        "categories": {
            "total": total_categories
        },
        "reviews": {
            "total": total_reviews,
            "approved": approved_reviews,
            "pending": pending_reviews
        },
        "routes": {
            "total": total_routes,
            "active": active_routes,
            "inactive": total_routes - active_routes
        },
        "users": {
            "total": total_users,
            "admins": admin_users,
            "regular": total_users - admin_users
        },
        "feedback": {
            "total": total_feedback,
            "unread": unread_feedback,
            "avg_rating": round(avg_website_rating, 1) if avg_website_rating else 0.0
        }
    }


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get all users (Admin only)
    """
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get single user by ID (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    new_role: str,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update user role (Admin only)
    """
    if new_role not in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'admin' or 'user'"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent changing own role
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    user.role = new_role
    db.commit()
    
    return {
        "message": f"User role updated to {new_role}",
        "user_id": user_id,
        "new_role": new_role,
        "success": True
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete user (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deleting own account
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return {
        "message": "User deleted successfully",
        "success": True
    }


@router.post("/users/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    new_password: str,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Reset user password (Admin only)
    """
    if len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.password = get_password_hash(new_password)
    db.commit()
    
    return {
        "message": "Password reset successfully",
        "user_id": user_id,
        "success": True
    }


@router.get("/activity/recent")
async def get_recent_activity(
    limit: int = 10,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get recent activity across the system (Admin only)
    """
    # Recent destinations
    recent_destinations = db.query(Destination)\
        .order_by(Destination.created_at.desc())\
        .limit(limit)\
        .all()
    
    # Recent reviews
    recent_reviews = db.query(Review)\
        .order_by(Review.created_at.desc())\
        .limit(limit)\
        .all()
    
    # Recent feedback
    recent_feedback = db.query(WebsiteFeedback)\
        .order_by(WebsiteFeedback.created_at.desc())\
        .limit(limit)\
        .all()
    
    # Recent users
    recent_users = db.query(User)\
        .order_by(User.created_at.desc())\
        .limit(limit)\
        .all()
    
    return {
        "destinations": [
            {
                "id": d.id,
                "name": d.name,
                "created_at": d.created_at,
                "type": "destination"
            } for d in recent_destinations
        ],
        "reviews": [
            {
                "id": r.id,
                "user_name": r.user_name,
                "rating": r.rating,
                "created_at": r.created_at,
                "type": "review"
            } for r in recent_reviews
        ],
        "feedback": [
            {
                "id": f.id,
                "user_name": f.user_name,
                "rating": f.rating,
                "created_at": f.created_at,
                "type": "feedback"
            } for f in recent_feedback
        ],
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "role": u.role,
                "created_at": u.created_at,
                "type": "user"
            } for u in recent_users
        ]
    }


@router.get("/reports/ratings")
async def get_ratings_report(
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed ratings report (Admin only)
    """
    # Top rated destinations
    top_destinations = db.query(
        Destination.id,
        Destination.name,
        Destination.rating,
        func.count(Review.id).label('review_count')
    ).outerjoin(Review)\
     .filter(Destination.is_active == True)\
     .group_by(Destination.id)\
     .order_by(Destination.rating.desc())\
     .limit(10)\
     .all()
    
    # Destinations needing attention (low rating)
    low_rated = db.query(
        Destination.id,
        Destination.name,
        Destination.rating,
        func.count(Review.id).label('review_count')
    ).outerjoin(Review)\
     .filter(
         Destination.is_active == True,
         Destination.rating < 3.0
     )\
     .group_by(Destination.id)\
     .order_by(Destination.rating.asc())\
     .limit(10)\
     .all()
    
    return {
        "top_rated": [
            {
                "id": d.id,
                "name": d.name,
                "rating": float(d.rating) if d.rating else 0.0,
                "review_count": d.review_count
            } for d in top_destinations
        ],
        "needs_attention": [
            {
                "id": d.id,
                "name": d.name,
                "rating": float(d.rating) if d.rating else 0.0,
                "review_count": d.review_count
            } for d in low_rated
        ]
    }


@router.post("/maintenance/cleanup")
async def cleanup_database(
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Clean up database (delete inactive/old records) (Admin only)
    """
    # This is a placeholder - implement carefully!
    return {
        "message": "Database cleanup feature - implement with caution!",
        "warning": "This feature should be implemented carefully with proper backups",
        "success": True
    }