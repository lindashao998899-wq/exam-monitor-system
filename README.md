# 双机考试监控系统（Dual-Machine Exam Monitor）

完整项目骨架：
- **教师机云桌面（React 控制台）**
- **学生机云桌面（Python Agent）**
- **中间服务端 API（FastAPI + WebSocket + PostgreSQL）**

## 1. 项目结构

```text
exam-monitor-system/
├── agent/
│   ├── agent_config.json
│   ├── start_student_agent.sh
│   ├── test_connectivity.sh
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
│   ├── package.json
│   └── vite.config.ts
├── scripts/
│   ├── bootstrap.sh
│   └── deploy_cloud.sh
└── docker-compose.yml
```

## 2. 云电脑部署方案（推荐）

> 场景：教师机和学生机是两台不同云桌面，通过内网互连。

### 2.1 教师机（部署后端 + 前端）

1) 拉取代码并进入目录：
```bash
cd /path/to/exam-monitor-system
```

2) 执行一键部署脚本（自动检测环境、创建配置、启动 DB、执行迁移、启动服务）：
```bash
./scripts/deploy_cloud.sh
```

3) 检查服务：
- 后端默认监听：`0.0.0.0:8000`
- 前端默认监听：`0.0.0.0:5173`
- 日志文件：
  - `backend/backend.log`
  - `frontend/frontend.log`

4) 如需修改端口/地址，编辑：
- `backend/.env`
- `frontend/.env`

### 2.2 学生机（启动 Agent）

1) 修改学生机配置文件：
```json
{
  "api_base": "http://<教师机内网IP>:8000/api",
  "session_id": 1
}
```
文件位置：`agent/agent_config.json`

2) 先做连通性测试：
```bash
./agent/test_connectivity.sh <教师机内网IP> 8000
```

3) 启动学生端：
```bash
./agent/start_student_agent.sh
```

4) 也可通过命令行覆盖配置：
```bash
./agent/start_student_agent.sh --api-base http://<教师机内网IP>:8000/api --session-id 1001
```

## 3. 防火墙 / 安全组端口开放

请在教师机云桌面（及其安全组）放通：
- `8000/TCP`：后端 API + WebSocket
- `5173/TCP`：前端开发服务（若生产用 Nginx 可改为 80/443）

如仅允许内网访问，建议限制来源网段为校园/考试内网 CIDR。

## 4. 跨机器访问说明

- 前端默认通过 Vite 代理 `/api` 和 `/ws` 到后端，避免跨域问题。
- 后端支持 `CORS_ORIGINS=*` 或自定义来源列表（逗号分隔）。
- 后端绑定地址可通过 `BACKEND_HOST` 配置，默认 `0.0.0.0`。

## 5. 本地开发（兼容原有方式）

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
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4) 启动前端
```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

5) 启动学生端 Agent
```bash
python agent/student_agent.py --config agent/agent_config.json
```

## 6. 后端能力（FastAPI）

### API 路由
- `POST /api/exams`：创建考试
- `GET /api/exams`：查询考试
- `PATCH /api/exams/{exam_id}/status`：开始/暂停/结束考试
- `POST /api/sessions/status`：学生机心跳与状态上报
- `POST /api/sessions/events`：学生机行为事件上报
- `POST /api/reports/{exam_id}/pdf`：导出 PDF
- `POST /api/reports/{exam_id}/excel`：导出 Excel
- `WS /ws/proctor`：实时监考状态推送

## 7. 后续建议
- 将 Agent 的锁屏/采集逻辑接入真实平台能力（Win/Mac/Linux）
- 增加鉴权（JWT + 设备签名）
- 导出服务替换为真实 PDF/Excel 模板渲染
- 增加实时告警策略（切屏、长时间无操作、人脸偏离）
