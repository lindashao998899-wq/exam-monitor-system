import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx

DEFAULT_CONFIG_PATH = Path(__file__).with_name("agent_config.json")


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


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="学生端监控 Agent")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="配置文件路径")
    parser.add_argument("--api-base", help="后端 API 地址，例如 http://10.10.0.10:8000/api")
    parser.add_argument("--session-id", type=int, help="考试会话 ID")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = load_config(Path(args.config))
    api_base = args.api_base or config.get("api_base") or "http://localhost:8000/api"
    session_id = args.session_id or int(config.get("session_id", 1))

    agent = StudentAgent(api_base=api_base, session_id=session_id)
    asyncio.run(agent.run())
