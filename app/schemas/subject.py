from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID

# ==========================================
# Subject Schemas
# ==========================================

class SubjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

class SubjectResponse(SubjectBase):
    id: UUID
    school_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# Teacher Assignment Schemas
# ==========================================

class TeacherAssignmentBase(BaseModel):
    role: str = Field(default="main_teacher", max_length=50)

class TeacherAssignmentCreate(TeacherAssignmentBase):
    teacher_id: UUID # User ID with teacher role
    classroom_id: UUID
    subject_id: UUID
    term_id: UUID

class TeacherAssignmentUpdate(BaseModel):
    role: Optional[str] = None
    teacher_id: Optional[UUID] = None
    subject_id: Optional[UUID] = None

class TeacherAssignmentResponse(TeacherAssignmentBase):
    id: UUID
    teacher_id: UUID
    classroom_id: UUID
    subject_id: UUID
    term_id: UUID
    
    model_config = ConfigDict(from_attributes=True)
