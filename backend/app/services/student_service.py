from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.models.student import Student, Enrollment
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate, EnrollmentCreate

class StudentService:
    """
    Service for managing Student profiles and Enrollments.
    """
    
    @staticmethod
    def create_student(db: Session, school_id: UUID, data: StudentCreate) -> Student:
        # Verify user exists and has student role
        user = db.query(User).filter(User.id == data.user_id).first()
        if not user or user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must exist and have 'student' role"
            )
            
        # Check if student profile already exists
        existing = db.query(Student).filter(Student.user_id == data.user_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student profile already exists for this user"
            )
            
        db_student = Student(**data.model_dump(), school_id=school_id)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def get_students(db: Session, school_id: UUID, classroom_id: Optional[UUID] = None) -> List[Student]:
        query = db.query(Student).filter(Student.school_id == school_id)
        if classroom_id:
            query = query.join(Enrollment).filter(Enrollment.classroom_id == classroom_id, Enrollment.status == "active")
        return query.all()

    @staticmethod
    def enroll_student(db: Session, data: EnrollmentCreate) -> Enrollment:
        # Simple enrollment logic - in a real system we'd check if term/classroom belong to same school
        db_enrollment = Enrollment(**data.model_dump())
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        return db_enrollment
