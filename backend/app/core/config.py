import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Dual-Machine Exam Monitor")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/exam_monitor",
    )
    ws_heartbeat_seconds: int = int(os.getenv("WS_HEARTBEAT_SECONDS", "10"))
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")


settings = Settings()
