# 双机考试监控系统（Dual-Machine Exam Monitor）

完整项目骨架：
- **A机教师控制台（React）**
- **B机学生端 Agent（Python）**
- **中间服务端 API（FastAPI + WebSocket + PostgreSQL）**

## 1. 项目结构

```text
exam-monitor-system/
├── agent/
│   └── student_agent.py
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── websocket/
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   └── main.tsx
│   └── package.json
├── scripts/
│   └── bootstrap.sh
└── docker-compose.yml
```

## 2. 后端能力（FastAPI）

### API 路由
- `POST /api/exams`：创建考试
- `GET /api/exams`：查询考试
- `PATCH /api/exams/{exam_id}/status`：开始/暂停/结束考试
- `POST /api/sessions/status`：B机心跳与状态上报
- `POST /api/sessions/events`：B机行为事件上报（answer_changed/question_submitted/proctor_*）
- `POST /api/reports/{exam_id}/pdf`：导出 PDF
- `POST /api/reports/{exam_id}/excel`：导出 Excel
- `WS /ws/proctor`：实时监考状态推送

### SQLAlchemy 模型（数据库表）
- `students`
- `devices`
- `exams`
- `exam_sessions`
- `questions`
- `question_snapshots`
- `answers`
- `answer_events`
- `proctor_events`
- `reports`

### 核心模块
- `app/services/scoring.py`：自动评分引擎（答案比对）
- `app/services/reporting.py`：报表生成骨架
- `app/websocket/manager.py`：WebSocket连接与广播管理

## 3. 前端能力（React）

教师控制台页面包含：
- 考试管理面板（创建/开始/暂停/结束）
- 实时监考面板（在线状态、当前题号、异常标记）
- 题目记录面板（截图、学生答案、正确答案、用时）
- 成绩分析面板（总分、正确率、错题、知识点统计）
- 复盘导出面板（PDF、Excel）

并通过 WebSocket 订阅实时监考数据。

## 4. B机 Agent（Python）

`agent/student_agent.py` 包含：
- 锁定考试窗口（骨架方法）
- 屏幕采集（骨架）
- 滚屏拼接截图（骨架）
- 作答行为监听与事件上报（answer_changed/question_submitted）
- 心跳状态上报

## 5. 本地启动（骨架）

1) 启动数据库
```bash
docker compose up -d
```

2) 安装依赖
```bash
./scripts/bootstrap.sh
```

3) 启动后端
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

4) 启动前端
```bash
cd frontend
npm run dev
```

5) 启动 B机 Agent
```bash
python agent/student_agent.py
```

## 6. 后续建议
- 增加 Alembic 迁移脚本与初始化数据
- 将 Agent 的锁屏/采集逻辑接入平台相关能力（Win/Mac/Linux）
- 增加鉴权（JWT + 设备签名）
- 将导出服务替换为真实 PDF/Excel 模板渲染
- 增加实时告警策略（切屏、长时间无操作、人脸偏离）
