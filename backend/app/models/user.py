from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base

class User(Base):
    """
    User model - represents users table in database.
    
    Users can be:
    - super_admin: Full system access
    - school_admin: Manage their school
    - teacher: Manage classes and grades
    - bursar: Financial management
    - accountant: View financial reports
    """
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    
    # School relationship (NULL for super_admin)
    school_id = Column(Uuid, ForeignKey("schools.id", ondelete="CASCADE"), nullable=True)
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Role and status
    role = Column(String(50), nullable=False)  # super_admin, school_admin, teacher, bursar, accountant
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # school = relationship("School", back_populates="users")
    
    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
    
    @property
    def full_name(self) -> str:
        """Return user's full name"""
        return f"{self.first_name} {self.last_name}"