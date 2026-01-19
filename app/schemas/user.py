from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# ==========================================
# Base Schema - Shared fields
# ==========================================

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: str = Field(..., description="User role: super_admin, school_admin, teacher, bursar, accountant")

# ==========================================
# Request Schemas (Input)
# ==========================================

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=100)
    school_id: Optional[UUID] = None  # Required except for super_admin
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@school.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+263771234567",
                "role": "teacher",
                "password": "SecurePass123!",
                "school_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    )

class UserUpdate(BaseModel):
    """Schema for updating user information"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+263771234567",
                "is_active": True
            }
        }
    )

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@school.com",
                "password": "SecurePass123!"
            }
        }
    )

# ==========================================
# Response Schemas (Output)
# ==========================================

class UserResponse(UserBase):
    """Schema for user data returned to client"""
    id: UUID
    school_id: Optional[UUID]
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserResponse):
    """Schema including password hash (internal use only)"""
    password_hash: str

# ==========================================
# Token Schemas
# ==========================================

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Data stored in JWT token"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None