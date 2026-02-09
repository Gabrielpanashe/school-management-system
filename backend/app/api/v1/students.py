from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.schemas.student import StudentCreate, StudentResponse, EnrollmentCreate, EnrollmentResponse
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Student Management"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "school_admin", "bursar"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return StudentService.create_student(db, current_user.school_id, data)

@router.get("/", response_model=List[StudentResponse])
def get_students(
    classroom_id: Optional[UUID] = None,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return StudentService.get_students(db, current_user.school_id, classroom_id)

@router.post("/enroll", response_model=EnrollmentResponse)
def enroll_student(data: EnrollmentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "school_admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return StudentService.enroll_student(db, data)
