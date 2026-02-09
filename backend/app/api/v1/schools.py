from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.schemas.school import SchoolCreate, SchoolUpdate, SchoolResponse
from app.services.school_service import SchoolService
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/schools", tags=["Schools"])

@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
def create_school(
    school_data: SchoolCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Register a new school.
    Only super_admin can register new schools.
    """
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can register schools"
        )
    return SchoolService.create_school(db, school_data)

@router.get("/", response_model=List[SchoolResponse])
def get_schools(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    List all schools.
    Only super_admin can list all schools.
    """
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can view all schools"
        )
    return SchoolService.get_all_schools(db, skip=skip, limit=limit)

@router.get("/{school_id}", response_model=SchoolResponse)
def get_school(
    school_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get school by ID.
    Users can only see their own school, unless they are super_admin.
    """
    if current_user.role != "super_admin" and current_user.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this school's data"
        )
        
    school = SchoolService.get_school_by_id(db, school_id)
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    return school

@router.patch("/{school_id}", response_model=SchoolResponse)
def update_school(
    school_id: UUID,
    school_data: SchoolUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update school details.
    Only super_admin or school_admin of that school can update.
    """
    if current_user.role != "super_admin" and (current_user.school_id != school_id or current_user.role != "school_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this school"
        )
        
    updated_school = SchoolService.update_school(db, school_id, school_data)
    if not updated_school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    return updated_school

@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(
    school_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a school.
    Only super_admin can delete schools.
    """
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete schools"
        )
        
    success = SchoolService.delete_school(db, school_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    return None
