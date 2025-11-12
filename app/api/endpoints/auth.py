# app/api/endpoints/auth.py - Authentication API Endpoints
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, UserLogin, UserResponse, Token, UserWithToken
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        user = AuthService.register_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/login", response_model=UserWithToken)
async def login(
    request: Request,
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return token"""
    user = AuthService.authenticate_user(
        db=db,
        username=credentials.username,
        password=credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Create access token
    access_token = AuthService.create_access_token(
        data={"user_id": user.id, "username": user.username}
    )
    
    # Store user_id in session (for web pages)
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role.value
    
    return UserWithToken(
        user=UserResponse.from_orm(user),
        token=Token(access_token=access_token)
    )


@router.post("/logout")
async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return current_user


@router.get("/check-session")
async def check_session(request: Request):
    """Check if user is logged in via session"""
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    role = request.session.get("role")
    
    if user_id:
        return {
            "logged_in": True,
            "user_id": user_id,
            "username": username,
            "role": role
        }
    
    return {"logged_in": False}