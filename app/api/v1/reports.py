from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID
from io import BytesIO

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reporting"])

@router.get("/report-card/{student_id}")
def get_report_card(
    student_id: UUID,
    term_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Generate and download a student's report card PDF.
    """
    # Authorization check... 
    # (Simplified: check if student belongs to same school as user)
    
    pdf_buffer = ReportService.generate_student_report_card(db, student_id, term_id)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_card_{student_id}.pdf"}
    )
