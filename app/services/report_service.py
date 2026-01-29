from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.student import Student
from app.models.academic import Term, Classroom
from app.services.attendance_service import AttendanceService
from app.services.grade_service import GradeService
from app.models.subject import Subject

class ReportService:
    """
    Service for generating PDF report cards.
    """
    
    @staticmethod
    def generate_student_report_card(db: Session, student_id: UUID, term_id: UUID) -> BytesIO:
        # 1. Fetch data
        student = db.query(Student).filter(Student.id == student_id).first()
        term = db.query(Term).filter(Term.id == term_id).first()
        # In a real app we'd fetch the user info linked to student
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Header
        elements.append(Paragraph(f"REPORT CARD - {term.name}", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Student Admission: {student.admission_number}", styles['Normal']))
        elements.append(Spacer(1, 24))
        
        # Attendance Summary
        att_summary = AttendanceService.get_student_attendance_summary(db, student_id, term_id)
        elements.append(Paragraph("Attendance Summary", styles['Heading2']))
        att_data = [
            ["Metric", "Value"],
            ["Total Days", str(att_summary["total_days"])],
            ["Present", str(att_summary["present"])],
            ["Absent", str(att_summary["absent"])],
            ["Percentage", f"{att_summary['attendance_percentage']}%"]
        ]
        t = Table(att_data, colWidths=[100, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 24))
        
        # Academic Performance
        elements.append(Paragraph("Academic Performance", styles['Heading2']))
        # Fetch subjects for this class
        # This is dynamic in a real app, here we simulate by fetching all subjects in school
        subjects = db.query(Subject).filter(Subject.school_id == student.school_id).all()
        
        perf_data = [["Subject", "Final %", "Status"]]
        for sub in subjects:
            res = GradeService.calculate_student_subject_grade(db, student_id, sub.id, term_id)
            perf_data.append([sub.name, f"{res['final_percentage']}%", res['status']])
            
        t2 = Table(perf_data, colWidths=[200, 100, 100])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t2)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
