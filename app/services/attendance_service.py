from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date
from uuid import UUID

from app.models.performance import Attendance
from app.schemas.performance import AttendanceCreate, AttendanceBulkCreate

class AttendanceService:
    """
    Service for managing student attendance.
    """
    
    @staticmethod
    def mark_attendance(db: Session, school_id: UUID, data: AttendanceCreate) -> Attendance:
        # Check if attendance already marked for this student on this date
        existing = db.query(Attendance).filter(
            Attendance.student_id == data.student_id,
            Attendance.date == data.date
        ).first()
        
        if existing:
            existing.status = data.status
            existing.remarks = data.remarks
            db.commit()
            db.refresh(existing)
            return existing
            
        db_attendance = Attendance(**data.model_dump(), school_id=school_id)
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance

    @staticmethod
    def bulk_mark_attendance(db: Session, school_id: UUID, data: AttendanceBulkCreate) -> List[Attendance]:
        results = []
        for entry in data.attendance_data:
            # Reusing the single mark logic
            att_data = AttendanceCreate(
                student_id=entry["student_id"],
                classroom_id=data.classroom_id,
                term_id=data.term_id,
                date=data.date,
                status=entry["status"],
                remarks=entry.get("remarks")
            )
            res = AttendanceService.mark_attendance(db, school_id, att_data)
            results.append(res)
        return results

    @staticmethod
    def get_classroom_attendance(db: Session, classroom_id: UUID, date: date) -> List[Attendance]:
        return db.query(Attendance).filter(
            Attendance.classroom_id == classroom_id,
            Attendance.date == date
        ).all()

    @staticmethod
    def get_student_attendance_summary(db: Session, student_id: UUID, term_id: UUID):
        records = db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.term_id == term_id
        ).all()
        
        total = len(records)
        present = len([r for r in records if r.status == "present"])
        late = len([r for r in records if r.status == "late"])
        absent = total - present - late
        
        percentage = (present + (late * 0.5)) / total * 100 if total > 0 else 0
        
        return {
            "total_days": total,
            "present": present,
            "late": late,
            "absent": absent,
            "attendance_percentage": round(percentage, 2)
        }
