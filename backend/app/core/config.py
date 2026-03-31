from dotenv import load_dotenv
import os

load_dotenv()


def _get_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_list(value: str | None, default: list[str] | None = None) -> list[str]:
    if value is None:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings:
    def __init__(self) -> None:
        self.app_name: str = "Dual-Machine Exam Monitor"
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://postgres:postgres@localhost:5432/exam_monitor",
        )
        self.cors_origins: list[str] = _get_list(
            os.getenv("CORS_ORIGINS"),
            ["http://localhost:5173", "http://127.0.0.1:5173"],
        )
        self.secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
        self.debug: bool = _get_bool(os.getenv("DEBUG"), default=False)
        self.ws_heartbeat_seconds: int = _get_int(
            os.getenv("WS_HEARTBEAT_SECONDS"),
            default=10,
        )


settings = Settings()
