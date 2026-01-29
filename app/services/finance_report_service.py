from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.models.student import Student
from app.models.finance import Payment, FeeStructure
from app.services.finance_service import FinanceService

class FinanceReportService:
    """
    Service for generating financial PDF reports (Receipts & Statements).
    """
    
    @staticmethod
    def generate_payment_receipt(db: Session, payment_id: UUID) -> BytesIO:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        student = db.query(Student).filter(Student.id == payment.student_id).first()
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Header
        elements.append(Paragraph("OFFICIAL PAYMENT RECEIPT", styles['Title']))
        elements.append(Spacer(1, 24))
        
        data = [
            ["Receipt ID:", str(payment.id)],
            ["Date:", payment.date.strftime("%Y-%m-%d %H:%M")],
            ["Student Admission:", student.admission_number],
            ["Payment Method:", payment.payment_method],
            ["Reference Number:", payment.reference_number or "N/A"],
            ["Amount Paid:", f"${payment.amount_paid:,.2f}"],
        ]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(t)
        
        elements.append(Spacer(1, 48))
        elements.append(Paragraph("Thank you for your payment.", styles['Italic']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
