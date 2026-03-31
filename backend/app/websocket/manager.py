from collections import defaultdict

from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, channel: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[channel].append(websocket)

    def disconnect(self, channel: str, websocket: WebSocket) -> None:
        if websocket in self.connections[channel]:
            self.connections[channel].remove(websocket)

    async def broadcast(self, channel: str, message: dict) -> None:
        for socket in list(self.connections[channel]):
            await socket.send_json(message)


ws_manager = WSConnectionManager()
