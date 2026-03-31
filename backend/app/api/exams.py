from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Exam
from app.schemas.exam import ExamCreate, ExamOut, ExamStatusUpdate

router = APIRouter(prefix="/exams", tags=["exams"])


@router.post("", response_model=ExamOut)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db)):
    exam = Exam(title=payload.title)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.get("", response_model=list[ExamOut])
def list_exams(db: Session = Depends(get_db)):
    return db.query(Exam).order_by(Exam.id.desc()).all()


@router.patch("/{exam_id}/status", response_model=ExamOut)
def update_exam_status(exam_id: int, payload: ExamStatusUpdate, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam.status = payload.status
    if payload.status == "running":
        exam.start_time = datetime.utcnow()
    if payload.status == "ended":
        exam.end_time = datetime.utcnow()

    db.commit()
    db.refresh(exam)
    return exam
