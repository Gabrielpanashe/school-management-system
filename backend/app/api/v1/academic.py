from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.schemas.academic import (
    AcademicYearCreate, AcademicYearResponse,
    TermCreate, TermResponse,
    ClassroomCreate, ClassroomResponse
)
from app.services.academic_service import AcademicService

router = APIRouter(prefix="/academic", tags=["Academic Management"])

# --- Academic Years ---

@router.post("/years", response_model=AcademicYearResponse, status_code=status.HTTP_201_CREATED)
def create_year(data: AcademicYearCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "school_admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return AcademicService.create_academic_year(db, current_user.school_id, data)

@router.get("/years", response_model=List[AcademicYearResponse])
def get_years(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return AcademicService.get_academic_years(db, current_user.school_id)

# --- Terms ---

@router.post("/terms", response_model=TermResponse, status_code=status.HTTP_201_CREATED)
def create_term(data: TermCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "school_admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return AcademicService.create_term(db, data)

# --- Classrooms ---

@router.post("/classrooms", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED)
def create_classroom(data: ClassroomCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "school_admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return AcademicService.create_classroom(db, current_user.school_id, data)

@router.get("/classrooms", response_model=List[ClassroomResponse])
def get_classrooms(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return AcademicService.get_classrooms(db, current_user.school_id)
