from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Date, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base

class AcademicYear(Base):
    """
    Academic Year Model - Represents a calendar/school year (e.g., 2026).
    """
    __tablename__ = "academic_years"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    school_id = Column(Uuid, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(100), nullable=False)  # "2026"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=False)
    
    # Relationships
    terms = relationship("Term", back_populates="academic_year", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AcademicYear {self.name}>"

class Term(Base):
    """
    Term Model - Represents periods within an academic year (e.g., Term 1, Semester 1).
    """
    __tablename__ = "terms"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    academic_year_id = Column(Uuid, ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(100), nullable=False)  # "First Term"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), default="upcoming")  # upcoming, active, completed
    
    # Relationships
    academic_year = relationship("AcademicYear", back_populates="terms")
    enrollments = relationship("Enrollment", back_populates="term")
    
    def __repr__(self):
        return f"<Term {self.name}>"

class Classroom(Base):
    """
    Classroom Model - Represents a specific grade and section (e.g., Grade 10-A).
    """
    __tablename__ = "classrooms"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    school_id = Column(Uuid, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(100), nullable=False)  # "Grade 10-A"
    grade_level = Column(String(50), nullable=False)  # "Grade 10"
    section = Column(String(50), nullable=True)  # "A"
    room_number = Column(String(50), nullable=True)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="classroom")
    
    def __repr__(self):
        return f"<Classroom {self.name}>"
