from datetime import datetime
from pathlib import Path


def generate_pdf_report(exam_id: int) -> str:
    folder = Path("reports")
    folder.mkdir(exist_ok=True)
    target = folder / f"exam_{exam_id}_{datetime.utcnow().timestamp():.0f}.pdf"
    target.write_bytes(b"%PDF-1.4\n% Skeleton report\n")
    return str(target)


def generate_excel_report(exam_id: int) -> str:
    folder = Path("reports")
    folder.mkdir(exist_ok=True)
    target = folder / f"exam_{exam_id}_{datetime.utcnow().timestamp():.0f}.xlsx"
    target.write_text("skeleton,report\n")
    return str(target)
