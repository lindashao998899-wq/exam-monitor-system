from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Dual-Machine Exam Monitor"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/exam_monitor"
    ws_heartbeat_seconds: int = 10


settings = Settings()
