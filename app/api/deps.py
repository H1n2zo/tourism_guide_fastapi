# app/api/deps.py - API Dependencies
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.auth_service import AuthService
from app.models.user import User, UserRole

security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user from JWT token or session.
    Returns None if not authenticated (for optional auth).
    """
    # Try JWT token first
    if credentials:
        try:
            payload = AuthService.verify_token(credentials.credentials)
            user_id = payload.get("user_id")
            if user_id:
                user = AuthService.get_user_by_id(db, user_id)
                if user:
                    return user
        except:
            pass
    
    # Try session as fallback
    user_id = request.session.get("user_id")
    if user_id:
        user = AuthService.get_user_by_id(db, user_id)
        if user:
            return user
    
    return None


async def require_current_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """
    Require authentication. Raises 401 if not authenticated.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


async def require_admin(
    current_user: User = Depends(require_current_user)
) -> User:
    """
    Require admin role. Raises 403 if not admin.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user