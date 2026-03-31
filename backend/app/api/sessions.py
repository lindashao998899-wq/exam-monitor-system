from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import AnswerEvent, ExamSession, ProctorEvent
from app.schemas.session import AgentEventPayload, SessionStatusPayload
from app.websocket.manager import ws_manager

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/status")
async def update_session_status(payload: SessionStatusPayload, db: Session = Depends(get_db)):
    session = db.query(ExamSession).filter(ExamSession.id == payload.session_id).first()
    if session:
        session.current_question_no = payload.current_question_no
        session.is_online = payload.is_online
        session.abnormal_flag = payload.abnormal_flag
        db.commit()

    await ws_manager.broadcast(
        "proctor",
        {
            "type": "session_status",
            "data": payload.model_dump(),
        },
    )
    return {"ok": True}


@router.post("/events")
async def collect_agent_event(payload: AgentEventPayload, db: Session = Depends(get_db)):
    if payload.event_type.startswith("proctor_"):
        event = ProctorEvent(
            session_id=payload.session_id,
            event_type=payload.event_type,
            details=payload.payload,
        )
    else:
        event = AnswerEvent(
            session_id=payload.session_id,
            question_id=payload.question_id,
            event_type=payload.event_type,
            payload=payload.payload,
        )
    db.add(event)
    db.commit()

    await ws_manager.broadcast("proctor", {"type": "event", "data": payload.model_dump()})
    return {"ok": True}
