from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate

class SchoolService:
    """
    School service - handles all school-related business logic.
    """
    
    @staticmethod
    def create_school(db: Session, school_data: SchoolCreate) -> School:
        """
        Create a new school entry in the database.
        """
        # Check if code already exists
        existing_school = db.query(School).filter(School.code == school_data.code).first()
        if existing_school:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"School with code {school_data.code} already exists"
            )
            
        db_school = School(
            name=school_data.name,
            code=school_data.code,
            address=school_data.address,
            phone=school_data.phone,
            email=school_data.email,
            logo_url=school_data.logo_url,
            subscription_status=school_data.subscription_status
        )
        
        db.add(db_school)
        db.commit()
        db.refresh(db_school)
        return db_school

    @staticmethod
    def get_school_by_id(db: Session, school_id: UUID) -> Optional[School]:
        """
        Retrieve a school by its ID.
        """
        return db.query(School).filter(School.id == school_id).first()

    @staticmethod
    def get_all_schools(db: Session, skip: int = 0, limit: int = 100) -> List[School]:
        """
        Retrieve all schools (useful for Super Admin).
        """
        return db.query(School).offset(skip).limit(limit).all()

    @staticmethod
    def update_school(db: Session, school_id: UUID, school_data: SchoolUpdate) -> Optional[School]:
        """
        Update school details.
        """
        db_school = SchoolService.get_school_by_id(db, school_id)
        if not db_school:
            return None
            
        # Update only provided fields
        update_data = school_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_school, key, value)
            
        db.commit()
        db.refresh(db_school)
        return db_school

    @staticmethod
    def delete_school(db: Session, school_id: UUID) -> bool:
        """
        Delete a school.
        """
        db_school = SchoolService.get_school_by_id(db, school_id)
        if not db_school:
            return False
            
        db.delete(db_school)
        db.commit()
        return True
