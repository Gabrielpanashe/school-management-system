from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.models.academic import AcademicYear, Term, Classroom
from app.schemas.academic import (
    AcademicYearCreate, AcademicYearUpdate,
    TermCreate, TermUpdate,
    ClassroomCreate, ClassroomUpdate
)

class AcademicService:
    """
    Service for managing Academic Years, Terms, and Classrooms.
    """
    
    # --- Academic Year Methods ---
    
    @staticmethod
    def create_academic_year(db: Session, school_id: UUID, data: AcademicYearCreate) -> AcademicYear:
        db_year = AcademicYear(**data.model_dump(), school_id=school_id)
        db.add(db_year)
        db.commit()
        db.refresh(db_year)
        return db_year

    @staticmethod
    def get_academic_years(db: Session, school_id: UUID) -> List[AcademicYear]:
        return db.query(AcademicYear).filter(AcademicYear.school_id == school_id).all()

    @staticmethod
    def get_academic_year(db: Session, year_id: UUID) -> Optional[AcademicYear]:
        return db.query(AcademicYear).filter(AcademicYear.id == year_id).first()

    # --- Term Methods ---

    @staticmethod
    def create_term(db: Session, data: TermCreate) -> Term:
        # Verify year exists
        year = db.query(AcademicYear).filter(AcademicYear.id == data.academic_year_id).first()
        if not year:
            raise HTTPException(status_code=404, detail="Academic year not found")
            
        db_term = Term(**data.model_dump())
        db.add(db_term)
        db.commit()
        db.refresh(db_term)
        return db_term

    @staticmethod
    def get_terms(db: Session, year_id: UUID) -> List[Term]:
        return db.query(Term).filter(Term.academic_year_id == year_id).all()

    # --- Classroom Methods ---

    @staticmethod
    def create_classroom(db: Session, school_id: UUID, data: ClassroomCreate) -> Classroom:
        db_classroom = Classroom(**data.model_dump(), school_id=school_id)
        db.add(db_classroom)
        db.commit()
        db.refresh(db_classroom)
        return db_classroom

    @staticmethod
    def get_classrooms(db: Session, school_id: UUID) -> List[Classroom]:
        return db.query(Classroom).filter(Classroom.school_id == school_id).all()

    @staticmethod
    def get_classroom(db: Session, classroom_id: UUID) -> Optional[Classroom]:
        return db.query(Classroom).filter(Classroom.id == classroom_id).first()
