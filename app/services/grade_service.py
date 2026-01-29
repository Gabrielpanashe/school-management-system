from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID
from sqlalchemy import func

from app.models.performance import Assessment, Grade
from app.schemas.performance import AssessmentCreate, GradeCreate, GradeBulkCreate

class GradeService:
    """
    Service for managing assessments and grades.
    """
    
    @staticmethod
    def create_assessment(db: Session, school_id: UUID, data: AssessmentCreate) -> Assessment:
        db_assessment = Assessment(**data.model_dump(), school_id=school_id)
        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)
        return db_assessment

    @staticmethod
    def enter_grade(db: Session, data: GradeCreate) -> Grade:
        # Check if grade already exists for this student and assessment
        existing = db.query(Grade).filter(
            Grade.student_id == data.student_id,
            Grade.assessment_id == data.assessment_id
        ).first()
        
        if existing:
            existing.marks_obtained = data.marks_obtained
            existing.remarks = data.remarks
            db.commit()
            db.refresh(existing)
            return existing
            
        db_grade = Grade(**data.model_dump())
        db.add(db_grade)
        db.commit()
        db.refresh(db_grade)
        return db_grade

    @staticmethod
    def bulk_enter_grades(db: Session, data: GradeBulkCreate) -> List[Grade]:
        results = []
        for entry in data.grades:
            grade_data = GradeCreate(
                student_id=entry["student_id"],
                assessment_id=data.assessment_id,
                marks_obtained=entry["marks_obtained"],
                remarks=entry.get("remarks")
            )
            res = GradeService.enter_grade(db, grade_data)
            results.append(res)
        return results

    @staticmethod
    def calculate_student_subject_grade(db: Session, student_id: UUID, subject_id: UUID, term_id: UUID):
        """
        Logic to compute weighted averages for a subject in a term.
        """
        # Get all assessments for this subject in this term
        assessments = db.query(Assessment).filter(
            Assessment.subject_id == subject_id,
            Assessment.term_id == term_id
        ).all()
        
        total_weighted_score = 0
        total_weight = 0
        
        for assessment in assessments:
            # Get student's grade for this assessment
            grade = db.query(Grade).filter(
                Grade.student_id == student_id,
                Grade.assessment_id == assessment.id
            ).first()
            
            if grade:
                percentage = (grade.marks_obtained / assessment.total_marks) * 100
                total_weighted_score += (percentage * (assessment.weight / 100))
                total_weight += assessment.weight
        
        final_percentage = (total_weighted_score / total_weight) * 100 if total_weight > 0 else 0
        
        return {
            "subject_id": subject_id,
            "final_percentage": round(final_percentage, 2),
            "status": "passed" if final_percentage >= 50 else "failed"
        }
