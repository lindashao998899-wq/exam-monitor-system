import asyncio
from datetime import datetime
from typing import Any

import httpx


class StudentAgent:
    def __init__(self, api_base: str, session_id: int):
        self.api_base = api_base.rstrip("/")
        self.session_id = session_id
        self.current_question_no = 1
        self.online = True

    async def lock_exam_window(self) -> None:
        print("[agent] lock exam window (skeleton)")

    async def capture_screen(self) -> str:
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        fake_path = f"captures/session_{self.session_id}_{ts}.png"
        print(f"[agent] captured screenshot: {fake_path}")
        return fake_path

    async def stitch_scroll_screenshots(self) -> str:
        merged = f"captures/session_{self.session_id}_stitched.png"
        print(f"[agent] stitched scrolling screenshots: {merged}")
        return merged

    async def emit_event(self, event_type: str, payload: dict[str, Any], question_id: int | None = None) -> None:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                f"{self.api_base}/sessions/events",
                json={
                    "session_id": self.session_id,
                    "event_type": event_type,
                    "question_id": question_id,
                    "payload": payload,
                },
            )

    async def heartbeat(self) -> None:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                f"{self.api_base}/sessions/status",
                json={
                    "session_id": self.session_id,
                    "current_question_no": self.current_question_no,
                    "is_online": self.online,
                    "abnormal_flag": False,
                },
            )

    async def monitor_answer_behavior(self) -> None:
        await self.emit_event("answer_changed", {"value": "A"}, question_id=1)
        await asyncio.sleep(1)
        await self.emit_event("question_submitted", {"value": "A", "cost": 12}, question_id=1)

    async def run(self) -> None:
        await self.lock_exam_window()
        while True:
            await self.heartbeat()
            await self.capture_screen()
            await self.stitch_scroll_screenshots()
            await self.monitor_answer_behavior()
            await asyncio.sleep(5)


if __name__ == "__main__":
    agent = StudentAgent(api_base="http://localhost:8000/api", session_id=1)
    asyncio.run(agent.run())
