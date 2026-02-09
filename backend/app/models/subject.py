from sqlalchemy import Column, String, ForeignKey, Uuid
from sqlalchemy.orm import relationship
import uuid

from app.db.database import Base

class Subject(Base):
    """
    Subject Model - Represents a curriculum subject (e.g., Mathematics, Physics).
    """
    __tablename__ = "subjects"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    school_id = Column(Uuid, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)  # "MATH101"
    description = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Subject {self.name} ({self.code})>"

class TeacherAssignment(Base):
    """
    TeacherAssignment Model - Assigns a teacher to a specific subject, classroom, and term.
    """
    __tablename__ = "teacher_assignments"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    teacher_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    classroom_id = Column(Uuid, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Uuid, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    term_id = Column(Uuid, ForeignKey("terms.id", ondelete="CASCADE"), nullable=False)
    
    role = Column(String(50), default="main_teacher")  # main_teacher, assistant, substitute
    
    def __repr__(self):
        return f"<Assignment Teacher:{self.teacher_id} Subject:{self.subject_id}>"
