from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.models.subject import Subject, TeacherAssignment
from app.models.user import User
from app.schemas.subject import SubjectCreate, SubjectUpdate, TeacherAssignmentCreate

class SubjectService:
    """
    Service for managing Subjects and Teacher Assignments.
    """
    
    @staticmethod
    def create_subject(db: Session, school_id: UUID, data: SubjectCreate) -> Subject:
        db_subject = Subject(**data.model_dump(), school_id=school_id)
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        return db_subject

    @staticmethod
    def get_subjects(db: Session, school_id: UUID) -> List[Subject]:
        return db.query(Subject).filter(Subject.school_id == school_id).all()

    @staticmethod
    def assign_teacher(db: Session, data: TeacherAssignmentCreate) -> TeacherAssignment:
        # Verify teacher role
        user = db.query(User).filter(User.id == data.teacher_id).first()
        if not user or user.role not in ["teacher", "school_admin"]:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user must have teacher or school_admin role"
            )
            
        db_assignment = TeacherAssignment(**data.model_dump())
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        return db_assignment
