from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# ==========================================
# Fee Structure Schemas
# ==========================================

class FeeStructureBase(BaseModel):
    classroom_id: UUID
    term_id: UUID
    total_amount: float = Field(..., gt=0)
    description: Optional[str] = None

class FeeStructureCreate(FeeStructureBase):
    pass

class FeeStructureUpdate(BaseModel):
    total_amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None

class FeeStructureResponse(FeeStructureBase):
    id: UUID
    school_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# Payment Schemas
# ==========================================

class PaymentBase(BaseModel):
    student_id: UUID
    term_id: UUID
    amount_paid: float = Field(..., gt=0)
    payment_method: str = Field(..., description="Cash, Bank, Mobile, etc.")
    reference_number: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: UUID
    school_id: UUID
    date: datetime
    recorded_by_id: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# Analytical/Report Schemas
# ==========================================

class FeeBalanceResponse(BaseModel):
    student_id: UUID
    term_id: UUID
    total_fees: float
    total_paid: float
    balance: float
    status: str # paid, partial, pending
