from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

# ==========================================
# Attendance Schemas
# ==========================================

class AttendanceBase(BaseModel):
    date: date
    status: str = Field(..., description="present, absent, late, excused")
    remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    student_id: UUID
    classroom_id: UUID
    term_id: UUID

class AttendanceBulkCreate(BaseModel):
    classroom_id: UUID
    term_id: UUID
    date: date
    attendance_data: List[dict] # List of {student_id, status, remarks}

class AttendanceResponse(AttendanceBase):
    id: UUID
    school_id: UUID
    student_id: UUID
    classroom_id: UUID
    term_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# Assessment Schemas
# ==========================================

class AssessmentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., description="exam, quiz, assignment, practical")
    total_marks: float
    weight: float = 100.0
    date: Optional[date] = None

class AssessmentCreate(AssessmentBase):
    classroom_id: UUID
    subject_id: UUID
    term_id: UUID

class AssessmentResponse(AssessmentBase):
    id: UUID
    school_id: UUID
    classroom_id: UUID
    subject_id: UUID
    term_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# Grade Schemas
# ==========================================

class GradeBase(BaseModel):
    marks_obtained: float
    remarks: Optional[str] = None

class GradeCreate(GradeBase):
    student_id: UUID
    assessment_id: UUID

class GradeBulkCreate(BaseModel):
    assessment_id: UUID
    grades: List[dict] # List of {student_id, marks_obtained, remarks}

class GradeResponse(GradeBase):
    id: UUID
    student_id: UUID
    assessment_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
