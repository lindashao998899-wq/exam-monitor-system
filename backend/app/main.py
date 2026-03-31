from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api import exams, reports, sessions
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.websocket.manager import ws_manager

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

allowed_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
allow_origin_regex = ".*" if settings.cors_origins.strip() == "*" else None

app.add_middleware(
    CORSMiddleware,
    allow_origins=[] if allow_origin_regex else allowed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exams.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.websocket("/ws/proctor")
async def proctor_channel(websocket: WebSocket):
    await ws_manager.connect("proctor", websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.broadcast("proctor", {"type": "echo", "data": data})
    except WebSocketDisconnect:
        ws_manager.disconnect("proctor", websocket)
