from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from uuid import UUID

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.schemas.performance import AttendanceResponse, AttendanceBulkCreate
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance Management"])

@router.post("/bulk", response_model=List[AttendanceResponse])
def bulk_mark_attendance(
    data: AttendanceBulkCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Bulk mark attendance for a classroom on a specific date.
    """
    # Authorization: Only teachers or admins
    if current_user.role not in ["super_admin", "school_admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    return AttendanceService.bulk_mark_attendance(db, current_user.school_id, data)

@router.get("/classroom/{classroom_id}", response_model=List[AttendanceResponse])
def get_classroom_attendance(
    classroom_id: UUID,
    date: date,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve attendance records for a specific classroom and date.
    """
    return AttendanceService.get_classroom_attendance(db, classroom_id, date)
