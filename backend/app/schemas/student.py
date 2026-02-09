from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

# ==========================================
# Student Schemas
# ==========================================

class StudentBase(BaseModel):
    admission_number: str = Field(..., min_length=1, max_length=50)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    guardian_name: Optional[str] = Field(None, max_length=200)
    guardian_phone: Optional[str] = Field(None, max_length=20)

class StudentCreate(StudentBase):
    user_id: UUID

class StudentUpdate(BaseModel):
    admission_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None

class StudentResponse(StudentBase):
    id: UUID
    user_id: UUID
    school_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# Enrollment Schemas
# ==========================================

class EnrollmentBase(BaseModel):
    status: str = Field(default="active")

class EnrollmentCreate(EnrollmentBase):
    student_id: UUID
    classroom_id: UUID
    term_id: UUID

class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None
    classroom_id: Optional[UUID] = None

class EnrollmentResponse(EnrollmentBase):
    id: UUID
    student_id: UUID
    classroom_id: UUID
    term_id: UUID
    enrolled_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
