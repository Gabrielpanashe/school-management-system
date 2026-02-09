from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# ==========================================
# Base Schema - Common fields all schemas share
# ==========================================

class SchoolBase(BaseModel):
    """
    Basic school information that all other schemas will use.
    Like a template with the common fields.
    """
    name: str = Field(..., min_length=1, max_length=255, description="School name")
    code: str = Field(..., min_length=1, max_length=50, description="Unique school code")
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    logo_url: Optional[str] = None

# ==========================================
# Request Schemas (What comes IN to API)
# ==========================================

class SchoolCreate(SchoolBase):
    """
    Schema for creating a NEW school.
    This is the form an admin fills out to add a school.
    """
    subscription_status: Optional[str] = Field(default="trial", description="trial, active, or suspended")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Greenwood High School",
                "code": "GHS001",
                "address": "123 Main Street, Harare",
                "phone": "+263771234567",
                "email": "info@greenwood.school",
                "subscription_status": "trial"
            }
        }
    )

class SchoolUpdate(BaseModel):
    """
    Schema for UPDATING an existing school.
    All fields are optional because you might only want to change one thing.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    logo_url: Optional[str] = None
    subscription_status: Optional[str] = None

# ==========================================
# Response Schemas (What goes OUT from API)
# ==========================================

class SchoolResponse(SchoolBase):
    """
    Schema for school data sent back to user.
    Includes everything including the ID and timestamps.
    """
    id: UUID
    subscription_status: str
    subscription_end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)