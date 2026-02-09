from sqlalchemy import Column, String, Date, ForeignKey, DateTime, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.database import Base

class Student(Base):
    """
    Student Model - Extended data for users with the 'student' role.
    """
    __tablename__ = "students"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    school_id = Column(Uuid, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    
    admission_number = Column(String(50), unique=True, nullable=False, index=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    guardian_name = Column(String(200), nullable=True)
    guardian_phone = Column(String(20), nullable=True)
    
    # Relationships
    # user = relationship("User", backref="student_profile")
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student {self.admission_number}>"

class Enrollment(Base):
    """
    Enrollment Model - Links a student to a classroom for a specific term.
    """
    __tablename__ = "enrollments"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    student_id = Column(Uuid, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    classroom_id = Column(Uuid, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    term_id = Column(Uuid, ForeignKey("terms.id", ondelete="CASCADE"), nullable=False)
    
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="active")  # active, withdrawn, suspended, completed
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    classroom = relationship("Classroom", back_populates="enrollments")
    term = relationship("Term", back_populates="enrollments")
    
    def __repr__(self):
        return f"<Enrollment Student:{self.student_id} Class:{self.classroom_id}>"
