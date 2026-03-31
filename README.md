# 双机考试监控系统（Dual-Machine Exam Monitor）

一个可直接运行的完整版本，包含：
- **前端教师控制台（React + Vite）**
- **后端 API 服务（FastAPI + WebSocket + PostgreSQL）**
- **学生端 Agent（Python 骨架）**
- **Docker 一键部署（frontend + backend + postgres）**

---

## 目录结构

```text
exam-monitor-system/
├── agent/
│   └── student_agent.py
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── alembic.ini
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── vite.config.ts
│   └── package.json
├── scripts/
│   └── bootstrap.sh
├── .env.example
└── docker-compose.yml
```

---

## 一、环境准备

建议环境：
- Docker / Docker Compose
- Python 3.11+
- Node.js 18+

安装依赖（自动检查环境并安装前后端依赖）：

```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

---

## 二、本地开发启动（不使用 Docker 跑前后端）

### 1) 启动数据库

```bash
cp .env.example .env
docker compose up -d postgres
```

### 2) 后端启动

```bash
cd backend
source ../.venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端健康检查：
- `http://localhost:8000/api/health`

### 3) 前端启动

```bash
cd frontend
npm run dev
```

前端地址：
- `http://localhost:5173`

---

## 三、Docker 一键部署（推荐）

### 1) 配置环境变量

```bash
cp .env.example .env
```

按需修改 `.env` 中的数据库账号密码、密钥、CORS 白名单等。

### 2) 启动全部服务

```bash
docker compose up -d --build
```

### 3) 访问地址

- 前端（Nginx）：`http://localhost:5173`
- 后端 API：`http://localhost:8000`
- 健康检查：`http://localhost:8000/api/health`

### 4) 常用运维命令

```bash
# 查看状态
docker compose ps

# 查看日志
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres

# 停止并删除容器
docker compose down
```

---

## 四、数据库迁移（Alembic）

已初始化 Alembic，首次运行：

```bash
cd backend
source ../.venv/bin/activate
alembic upgrade head
```

后续新增模型后可生成迁移：

```bash
alembic revision --autogenerate -m "your migration message"
alembic upgrade head
```

---

## 五、主要环境变量说明

详见 `.env.example`：

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `SECRET_KEY`
- `DEBUG`
- `WS_HEARTBEAT_SECONDS`

---

## 六、功能概览

- 教师端考试管理（创建/状态切换）
- 学生端状态与行为事件上报
- WebSocket 实时监考数据广播
- PDF / Excel 报表导出骨架
- Docker Compose 一键启动全栈服务

