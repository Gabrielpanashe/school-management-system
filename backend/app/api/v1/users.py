from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.schemas.user import UserResponse
from app.models.user import User

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/", response_model=List[UserResponse])
def get_users(
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    List users in the school.
    Allows filtering by role (e.g., teacher, bursar).
    """
    query = db.query(User).filter(User.school_id == current_user.school_id)
    
    if role:
        query = query.filter(User.role == role)
        
    return query.all()
