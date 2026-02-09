from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Text, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base

class FeeStructure(Base):
    """
    FeeStructure Model - Defines the total amount due for a specific Classroom and Term.
    """
    __tablename__ = "fee_structures"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    school_id = Column(Uuid, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    classroom_id = Column(Uuid, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    term_id = Column(Uuid, ForeignKey("terms.id", ondelete="CASCADE"), nullable=False)
    
    total_amount = Column(Float, nullable=False) # Total fees for this class/term
    description = Column(Text, nullable=True) # Breakdown or notes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FeeStructure Class:{self.classroom_id} Term:{self.term_id} Amount:{self.total_amount}>"

class Payment(Base):
    """
    Payment Model - Records a financial transaction made by a student.
    """
    __tablename__ = "payments"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    school_id = Column(Uuid, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Uuid, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    term_id = Column(Uuid, ForeignKey("terms.id", ondelete="CASCADE"), nullable=False)
    
    amount_paid = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(50), nullable=False) # Cash, Bank, Mobile, etc.
    reference_number = Column(String(100), unique=True, nullable=True) # Transaction ID
    
    # Audit: Who recorded this payment?
    recorded_by_id = Column(Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Payment Student:{self.student_id} Amount:{self.amount_paid} Date:{self.date}>"
