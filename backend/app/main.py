from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api import exams, reports, sessions
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.websocket.manager import ws_manager

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exams.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": settings.app_name}


@app.websocket("/ws/proctor")
async def proctor_channel(websocket: WebSocket):
    await ws_manager.connect("proctor", websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.broadcast("proctor", {"type": "echo", "data": data})
    except WebSocketDisconnect:
        ws_manager.disconnect("proctor", websocket)
