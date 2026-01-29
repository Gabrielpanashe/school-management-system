from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.schemas.performance import AssessmentCreate, AssessmentResponse, GradeBulkCreate, GradeResponse
from app.services.grade_service import GradeService

router = APIRouter(prefix="/grades", tags=["Grade Management"])

@router.post("/assessments", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_assessment(
    data: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new assessment (Exam, Quiz, etc.)
    """
    if current_user.role not in ["super_admin", "school_admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return GradeService.create_assessment(db, current_user.school_id, data)

@router.post("/bulk-enter", response_model=List[GradeResponse])
def bulk_enter_grades(
    data: GradeBulkCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Batch enter grades for students in an assessment.
    """
    if current_user.role not in ["super_admin", "school_admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return GradeService.bulk_enter_grades(db, data)
