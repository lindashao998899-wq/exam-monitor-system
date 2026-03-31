from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.api import exams, reports, sessions
from app.db.base import Base
from app.db.session import engine
from app.websocket.manager import ws_manager

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dual-Machine Exam Monitor API")
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
