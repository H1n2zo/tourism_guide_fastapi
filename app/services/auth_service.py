# app/services/auth_service.py - FIXED Authentication Service
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.config import settings

# Password hashing - Support both PHP bcrypt ($2y$) and Python bcrypt ($2b$)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b"  # Use $2b$ for new hashes
)


class AuthService:
    """Authentication service for user management - FIXED"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash - FIXED to support PHP bcrypt"""
        try:
            # Convert to string if needed
            hash_str = str(hashed_password)
            
            # PHP uses $2y$, Python's passlib uses $2b$
            # They're compatible, just replace the identifier
            if hash_str.startswith('$2y$'):
                hash_str = '$2b$' + hash_str[4:]
            
            return pwd_context.verify(plain_password, hash_str)
        except Exception as e:
            print(f"Password verification error: {e}")
            return False
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password - FIXED"""
        try:
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                print(f"User not found: {username}")
                return None
            
            # Get password as string
            stored_password = str(user.password)
            print(f"Verifying password for user: {username}")
            
            if not AuthService.verify_password(password, stored_password):
                print(f"Password verification failed for user: {username}")
                return None
            
            print(f"User authenticated successfully: {username}")
            return user
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    @staticmethod
    def register_user(db: Session, username: str, email: str, password: str) -> User:
        """Register a new user - FIXED"""
        try:
            # Check if username exists
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            
            # Check if email exists
            if email:
                existing_email = db.query(User).filter(User.email == email).first()
                if existing_email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
            
            # Hash password
            hashed_password = AuthService.get_password_hash(password)
            print(f"Creating user: {username} with hashed password")
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role=UserRole.USER
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print(f"User created successfully: {username} (ID: {new_user.id})")
            return new_user
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            print(f"Registration error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {str(e)}"
            )
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()