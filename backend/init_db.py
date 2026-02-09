from app.db.database import engine, Base
from app.models.school import School
from app.models.user import User
from app.models.academic import AcademicYear, Term, Classroom
from app.models.student import Student, Enrollment
from app.models.subject import Subject, TeacherAssignment
from app.models.performance import Attendance, Assessment, Grade
from app.models.finance import FeeStructure, Payment

print("Initializing local SQLite database...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
