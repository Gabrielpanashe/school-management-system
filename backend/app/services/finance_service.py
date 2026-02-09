from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID
from sqlalchemy import func

from app.models.finance import FeeStructure, Payment
from app.models.student import Student, Enrollment
from app.schemas.finance import FeeStructureCreate, PaymentCreate

class FinanceService:
    """
    Service for managing school finances (Fees and Payments).
    """
    
    # --- Fee Structure Setup ---
    
    @staticmethod
    def setup_fee_structure(db: Session, school_id: UUID, data: FeeStructureCreate) -> FeeStructure:
        # Check if structure already exists for this classroom and term
        existing = db.query(FeeStructure).filter(
            FeeStructure.classroom_id == data.classroom_id,
            FeeStructure.term_id == data.term_id
        ).first()
        
        if existing:
            existing.total_amount = data.total_amount
            existing.description = data.description
            db.commit()
            db.refresh(existing)
            return existing
            
        db_structure = FeeStructure(**data.model_dump(), school_id=school_id)
        db.add(db_structure)
        db.commit()
        db.refresh(db_structure)
        return db_structure

    @staticmethod
    def get_fee_structures(db: Session, school_id: UUID) -> List[FeeStructure]:
        return db.query(FeeStructure).filter(FeeStructure.school_id == school_id).all()

    # --- Payment Recording ---

    @staticmethod
    def record_payment(db: Session, school_id: UUID, recorder_id: UUID, data: PaymentCreate) -> Payment:
        # 1. Verify student exists
        student = db.query(Student).filter(Student.id == data.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
            
        # 2. Record the payment
        db_payment = Payment(
            **data.model_dump(),
            school_id=school_id,
            recorded_by_id=recorder_id
        )
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment

    @staticmethod
    def get_student_payments(db: Session, student_id: UUID, term_id: Optional[UUID] = None) -> List[Payment]:
        query = db.query(Payment).filter(Payment.student_id == student_id)
        if term_id:
            query = query.filter(Payment.term_id == term_id)
        return query.all()

    @staticmethod
    def get_all_payments(db: Session, school_id: UUID, limit: int = 50) -> List[Payment]:
        return db.query(Payment).filter(Payment.school_id == school_id).order_by(Payment.payment_date.desc()).limit(limit).all()

    @staticmethod
    def get_revenue_stats(db: Session, school_id: UUID):
        # Total revenue collected
        total_revenue = db.query(func.sum(Payment.amount_paid)).filter(Payment.school_id == school_id).scalar() or 0
        
        # This month's revenue
        from datetime import date
        today = date.today()
        month_start = date(today.year, today.month, 1)
        monthly_revenue = db.query(func.sum(Payment.amount_paid)).filter(
            Payment.school_id == school_id,
            Payment.payment_date >= month_start
        ).scalar() or 0
        
        return {
            "total_revenue": total_revenue,
            "monthly_revenue": monthly_revenue,
            # We could add more complex trends here later
        }

    # --- Balance Calculations ---

    @staticmethod
    def get_student_fee_balance(db: Session, student_id: UUID, term_id: UUID):
        # 1. Find the student's classroom for this term
        enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.term_id == term_id
        ).first()
        
        if not enrollment:
            return {
                "total_fees": 0,
                "total_paid": 0,
                "balance": 0,
                "status": "pending"
            }
            
        # 2. Get the fee structure for that classroom and term
        fee_structure = db.query(FeeStructure).filter(
            FeeStructure.classroom_id == enrollment.classroom_id,
            FeeStructure.term_id == term_id
        ).first()
        
        total_fees = fee_structure.total_amount if fee_structure else 0
        
        # 3. Sum all payments made by this student for this term
        total_paid = db.query(func.sum(Payment.amount_paid)).filter(
            Payment.student_id == student_id,
            Payment.term_id == term_id
        ).scalar() or 0
        
        balance = total_fees - total_paid
        
        status = "paid" if balance <= 0 and total_fees > 0 else "partial" if total_paid > 0 else "pending"
        
        return {
            "student_id": student_id,
            "term_id": term_id,
            "total_fees": total_fees,
            "total_paid": total_paid,
            "balance": max(0, balance),
            "status": status
        }
