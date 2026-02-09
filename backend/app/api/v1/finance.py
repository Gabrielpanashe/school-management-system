from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.schemas.finance import (
    FeeStructureCreate, FeeStructureResponse,
    PaymentCreate, PaymentResponse,
    FeeBalanceResponse
)
from app.services.finance_service import FinanceService

router = APIRouter(prefix="/finance", tags=["Fee Management & Payments"])

# --- Fee Structures ---

@router.post("/structures", response_model=FeeStructureResponse, status_code=status.HTTP_201_CREATED)
def create_fee_structure(
    data: FeeStructureCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Define or update fee structure for a classroom and term.
    Only bursars or admins.
    """
    if current_user.role not in ["super_admin", "school_admin", "bursar"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return FinanceService.setup_fee_structure(db, current_user.school_id, data)

@router.get("/structures", response_model=List[FeeStructureResponse])
def get_fee_structures(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return FinanceService.get_fee_structures(db, current_user.school_id)

# --- Payments ---

@router.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def record_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Record a student payment.
    Sensitive: Only bursars or admins.
    """
    if current_user.role not in ["super_admin", "school_admin", "bursar"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return FinanceService.record_payment(db, current_user.school_id, current_user.id, data)

@router.get("/payments/student/{student_id}", response_model=List[PaymentResponse])
def get_student_payments(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get payment history for a specific student.
    """
    # Authorization: User can see their own payments (if student) or staff can see all
    if current_user.role == "student" and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Cannot view other students' payments")
        
    return FinanceService.get_student_payments(db, student_id)

# --- Balances ---

@router.get("/balance/{student_id}", response_model=FeeBalanceResponse)
def get_student_balance(
    student_id: UUID,
    term_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Calculate real-time fee balance for a student.
    """
    return FinanceService.get_student_fee_balance(db, student_id, term_id)
