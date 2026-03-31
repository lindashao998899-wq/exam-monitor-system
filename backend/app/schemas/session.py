from pydantic import BaseModel


class SessionStatusPayload(BaseModel):
    session_id: int
    current_question_no: int
    is_online: bool
    abnormal_flag: bool = False


class AgentEventPayload(BaseModel):
    session_id: int
    event_type: str
    question_id: int | None = None
    payload: dict
