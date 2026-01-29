from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.schemas.subject import SubjectCreate, SubjectResponse, TeacherAssignmentCreate, TeacherAssignmentResponse
from app.services.subject_service import SubjectService

router = APIRouter(prefix="/subjects", tags=["Subject & Teacher Management"])

@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(data: SubjectCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "school_admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return SubjectService.create_subject(db, current_user.school_id, data)

@router.get("/", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return SubjectService.get_subjects(db, current_user.school_id)

@router.post("/assign-teacher", response_model=TeacherAssignmentResponse)
def assign_teacher(data: TeacherAssignmentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "school_admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return SubjectService.assign_teacher(db, data)
