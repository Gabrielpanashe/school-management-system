from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date
from uuid import UUID

# ==========================================
# Academic Year Schemas
# ==========================================

class AcademicYearBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    start_date: date
    end_date: date
    is_current: bool = False

class AcademicYearCreate(AcademicYearBase):
    pass

class AcademicYearUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None

class AcademicYearResponse(AcademicYearBase):
    id: UUID
    school_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# Term Schemas
# ==========================================

class TermBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    start_date: date
    end_date: date
    status: str = Field(default="upcoming") # upcoming, active, completed

class TermCreate(TermBase):
    academic_year_id: UUID

class TermUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class TermResponse(TermBase):
    id: UUID
    academic_year_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# Classroom Schemas
# ==========================================

class ClassroomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    grade_level: str = Field(..., max_length=50)
    section: Optional[str] = Field(None, max_length=50)
    room_number: Optional[str] = Field(None, max_length=50)

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomUpdate(BaseModel):
    name: Optional[str] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None
    room_number: Optional[str] = None

class ClassroomResponse(ClassroomBase):
    id: UUID
    school_id: UUID
    
    model_config = ConfigDict(from_attributes=True)
