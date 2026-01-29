from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.services.finance_report_service import FinanceReportService

router = APIRouter(prefix="/finance-reports", tags=["Financial Reporting"])

@router.get("/receipt/{payment_id}")
def download_receipt(
    payment_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Download a PDF receipt for a payment.
    """
    # Sensitivity check: Only staff or the student who paid can download
    if current_user.role not in ["super_admin", "school_admin", "bursar", "student"]:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    pdf_buffer = FinanceReportService.generate_payment_receipt(db, payment_id)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=receipt_{payment_id}.pdf"}
    )
