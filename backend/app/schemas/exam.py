from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExamCreate(BaseModel):
    title: str


class ExamStatusUpdate(BaseModel):
    status: str


class ExamOut(BaseModel):
    id: int
    title: str
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True
