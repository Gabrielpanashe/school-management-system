from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.database import Base

class School(Base):
    """
    School Model - Represents a school in our system.
    
    Think of this like a school's ID card. It has:
    - School name (e.g., "Greenwood High School")
    - School code (e.g., "GHS001" - like a short nickname)
    - Contact information (address, phone, email)
    - Subscription info (is the school paying to use our system?)
    """
    
    __tablename__ = "schools"
    
    # Primary Key - Unique ID for this school
    # Like a student ID number, but for schools
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Information
    name = Column(String(255), nullable=False)  # "ST Martin's School"
    code = Column(String(50), unique=True, nullable=False)  # "GHS001"
    
    # Contact Information
    address = Column(String, nullable=True)  # "123 st martin, Harare"
    phone = Column(String(20), nullable=True)  # "+263771234567"
    email = Column(String(255), nullable=True)  # "info@atmartins.school"
    
    # Logo (URL to image)
    logo_url = Column(String, nullable=True)  # Link to school logo
    
    # Subscription Information
    # Is the school paying? trial/active/suspended
    subscription_status = Column(String(50), default='trial')
    subscription_end_date = Column(DateTime, nullable=True)
    
    # Timestamps - When was this created/updated?
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """What to show when we print this school"""
        return f"<School {self.name} ({self.code})>"