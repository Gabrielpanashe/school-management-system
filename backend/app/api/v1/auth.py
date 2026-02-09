from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.utils.security import decode_access_token

# ==========================================
# Router Setup
# ==========================================

# Think of router like a mailbox for auth-related requests
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Security scheme - checks for "Bearer token" in requests
security = HTTPBearer()

# ==========================================
# Dependency: Get Current User
# ==========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    This function checks if someone is logged in.
    
    How it works:
    1. User sends their token (like showing an ID card)
    2. We decode the token (check if ID card is real)
    3. We find the user in database
    4. Return the user
    
    If ANY step fails = "You're not logged in!"
    """
    # Get the token from the request
    token = credentials.credentials
    
    # Decode the token to get user info
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user_id from token
    user_id: str = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    # Find user in database
    user = AuthService.get_user_by_id(db, user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user

# ==========================================
# ENDPOINT 1: Register New User
# ==========================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user account.
    
    Like filling out a registration form for a new teacher or admin.
    
    Steps:
    1. Receive user data (email, password, name, etc.)
    2. Check if email already exists (no duplicates!)
    3. Hash the password (scramble it for security)
    4. Save to database
    5. Return the new user (WITHOUT the password!)
    """
    new_user = AuthService.create_user(db, user_data)
    return new_user

# ==========================================
# ENDPOINT 2: Login
# ==========================================

@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login and get an access token.
    
    Like showing your ID and password at the school gate.
    If correct, you get a visitor badge (token) to enter.
    
    Steps:
    1. Receive email and password
    2. Find user by email
    3. Check if password matches
    4. Create a token (visitor badge)
    5. Return the token
    """
    # Try to authenticate
    user = AuthService.authenticate_user(db, credentials)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token for this user
    access_token = AuthService.create_token_for_user(user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ==========================================
# ENDPOINT 3: Get Current User Info
# ==========================================

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    """
    Get information about the currently logged-in user.
    
    Like looking at your student ID card to see your info.
    
    This endpoint is PROTECTED - you must be logged in to use it.
    """
    return current_user