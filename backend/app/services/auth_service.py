from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
import uuid

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import verify_password, get_password_hash, create_access_token

class AuthService:
    """
    Authentication service - handles all auth-related business logic.
    Separating this from API routes makes code cleaner and more testable.
    """
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            db: Database session
            user_data: User creation data
        
        Returns:
            Created user object
        
        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validate school_id requirement (except for super_admin)
        if user_data.role != "super_admin" and not user_data.school_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="school_id is required for non-super_admin users"
            )
        
        # Create new user with hashed password
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            role=user_data.role,
            school_id=user_data.school_id,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            db: Database session
            login_data: Login credentials
        
        Returns:
            User object if authentication successful, None otherwise
        """
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user:
            return None
        
        if not verify_password(login_data.password, user.password_hash):
            return None
        
        if not user.is_active:
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def create_token_for_user(user: User) -> str:
        """
        Create JWT access token for a user.
        
        Args:
            user: User object
        
        Returns:
            JWT token string
        """
        token_data = {
            "sub": str(user.id),  # 'sub' is standard claim for subject/user_id
            "email": user.email,
            "role": user.role,
        }
        
        access_token = create_access_token(data=token_data)
        return access_token
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        """
        if isinstance(user_id, str):
            try:
                user_id = uuid.UUID(user_id)
            except ValueError:
                pass
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            db: Database session
            email: User email
        
        Returns:
            User object or None
        """
        return db.query(User).filter(User.email == email).first()
