from fastapi import APIRouter

from app.services.reporting import generate_excel_report, generate_pdf_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/{exam_id}/pdf")
def export_pdf_report(exam_id: int):
    return {"file": generate_pdf_report(exam_id)}


@router.post("/{exam_id}/excel")
def export_excel_report(exam_id: int):
    return {"file": generate_excel_report(exam_id)}
