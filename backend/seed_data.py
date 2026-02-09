import uuid
from datetime import date, datetime, timedelta
from app.db.database import SessionLocal, engine, Base
from app.models.school import School
from app.models.user import User
from app.models.academic import AcademicYear, Term, Classroom
from app.models.student import Student, Enrollment
from app.models.subject import Subject, TeacherAssignment
from app.models.performance import Attendance, Assessment, Grade
from app.models.finance import FeeStructure, Payment
from app.utils.security import get_password_hash

def seed():
    db = SessionLocal()
    
    try:
        print("🌱 Seeding data...")
        
        # 1. Create School
        school = School(
            name="St. Martin's Academy",
            code="SMA001",
            address="123 Education Way, Harare",
            phone="+263771234567",
            email="info@stmartins.edu",
            subscription_status="active"
        )
        db.add(school)
        db.flush() # Get school ID
        
        print(f"✅ School created: {school.name}")
        
        # 2. Create Users
        admin = User(
            email="admin@stmartins.com",
            password_hash=get_password_hash("Admin123!"),
            first_name="Admin",
            last_name="User",
            role="school_admin",
            school_id=school.id
        )
        
        teacher1 = User(
            email="john.doe@stmartins.com",
            password_hash=get_password_hash("Teacher123!"),
            first_name="John",
            last_name="Doe",
            role="teacher",
            school_id=school.id
        )
        
        teacher2 = User(
            email="jane.smith@stmartins.com",
            password_hash=get_password_hash("Teacher123!"),
            first_name="Jane",
            last_name="Smith",
            role="teacher",
            school_id=school.id
        )
        
        bursar = User(
            email="sarah.jones@stmartins.com",
            password_hash=get_password_hash("Bursar123!"),
            first_name="Sarah",
            last_name="Jones",
            role="bursar",
            school_id=school.id
        )
        
        db.add_all([admin, teacher1, teacher2, bursar])
        db.flush()
        
        print("✅ Users created: Admin, Teachers, Bursar")
        
        # 3. Academic Setup
        year_2026 = AcademicYear(
            school_id=school.id,
            name="2026",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            is_current=True
        )
        db.add(year_2026)
        db.flush()
        
        term1 = Term(
            academic_year_id=year_2026.id,
            name="Term 1",
            start_date=date(2026, 1, 12),
            end_date=date(2026, 4, 10),
            status="active"
        )
        db.add(term1)
        db.flush()
        
        classroom1 = Classroom(
            school_id=school.id,
            name="Grade 1-A",
            grade_level="Grade 1",
            section="A",
            room_number="R101"
        )
        db.add(classroom1)
        db.flush()
        
        print("✅ Academic setup: Year 2026, Term 1, Grade 1-A")
        
        # 4. Subjects
        math = Subject(school_id=school.id, name="Mathematics", code="MATH01")
        english = Subject(school_id=school.id, name="English", code="ENG01")
        db.add_all([math, english])
        db.flush()
        
        # Assignments
        assign1 = TeacherAssignment(
            teacher_id=teacher1.id,
            classroom_id=classroom1.id,
            subject_id=math.id,
            term_id=term1.id
        )
        db.add(assign1)
        
        print("✅ Subjects and Teacher Assignments created")
        
        # 5. Students
        students_data = [
            ("Alice", "Brown", "STU001"),
            ("Bob", "Wilson", "STU002"),
            ("Charlie", "Davis", "STU003"),
            ("David", "Miller", "STU004"),
            ("Eve", "White", "STU005")
        ]
        
        for fname, lname, ad_no in students_data:
            # Create user for student
            stu_user = User(
                email=f"{fname.lower()}.{lname.lower()}@stmartins.com",
                password_hash=get_password_hash("Student123!"),
                first_name=fname,
                last_name=lname,
                role="student",
                school_id=school.id
            )
            db.add(stu_user)
            db.flush()
            
            # Create student profile
            student = Student(
                user_id=stu_user.id,
                school_id=school.id,
                admission_number=ad_no,
                gender="Other",
                date_of_birth=date(2018, 5, 20)
            )
            db.add(student)
            db.flush()
            
            # Enroll in class
            enrollment = Enrollment(
                student_id=student.id,
                classroom_id=classroom1.id,
                term_id=term1.id
            )
            db.add(enrollment)
            
            # Add some attendance (Mark all as present for today)
            att = Attendance(
                school_id=school.id,
                student_id=student.id,
                classroom_id=classroom1.id,
                term_id=term1.id,
                status="present",
                date=date.today()
            )
            db.add(att)
            
        print(f"✅ Created {len(students_data)} students with enrollment and attendance")
        
        # 6. Finance
        fee = FeeStructure(
            school_id=school.id,
            classroom_id=classroom1.id,
            term_id=term1.id,
            total_amount=1500.0,
            description="Tuition: $1200, Sports: $300"
        )
        db.add(fee)
        
        # Add a sample payment for one student
        sample_stu = db.query(Student).filter(Student.admission_number == "STU001").first()
        payment = Payment(
            school_id=school.id,
            student_id=sample_stu.id,
            term_id=term1.id,
            amount_paid=500.0,
            payment_method="Bank Transfer",
            reference_number=str(uuid.uuid4())[:8].upper(),
            recorded_by_id=bursar.id
        )
        db.add(payment)
        
        print("✅ Financials: Fee structures and 1st payment created")
        
        db.commit()
        print("\n🚀 Seeding successful! You can now login with:")
        print("   Email: admin@stmartins.com")
        print("   Password: Admin123!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
