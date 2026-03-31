#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "========== 双机考试监控系统：云电脑一键部署 =========="

ensure_file() {
  local file_path="$1"
  local file_content="$2"
  if [ ! -f "${file_path}" ]; then
    echo "[创建] ${file_path}"
    printf "%s\n" "${file_content}" > "${file_path}"
  else
    echo "[检测] ${file_path} 已存在，跳过创建"
  fi
}

echo "[1/6] 检测运行环境..."
command -v python >/dev/null 2>&1 || { echo "[错误] 未找到 python"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "[错误] 未找到 docker"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "[错误] 未找到 npm"; exit 1; }

echo "[2/6] 生成默认配置文件..."
ensure_file "backend/.env" "BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=*
DATABASE_URL=postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/exam_monitor"

ensure_file "frontend/.env" "VITE_PROXY_TARGET=http://127.0.0.1:8000
VITE_API_BASE_URL=/api"

ensure_file "agent/agent_config.json" "{
  \"api_base\": \"http://127.0.0.1:8000/api\",
  \"session_id\": 1
}"

echo "[3/6] 安装依赖..."
./scripts/bootstrap.sh

echo "[4/6] 启动数据库（PostgreSQL）..."
docker compose up -d postgres

echo "[5/6] 执行数据库迁移..."
set -a
# shellcheck disable=SC1091
source backend/.env
set +a
PYTHONPATH=backend python -m app.db.migrate

echo "[6/6] 启动服务..."
BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}" BACKEND_PORT="${BACKEND_PORT:-8000}" nohup ./.venv/bin/uvicorn app.main:app --app-dir backend --host "${BACKEND_HOST}" --port "${BACKEND_PORT}" > backend/backend.log 2>&1 &
nohup npm --prefix frontend run dev -- --host 0.0.0.0 > frontend/frontend.log 2>&1 &

echo "部署完成："
echo "- 后端日志: backend/backend.log"
echo "- 前端日志: frontend/frontend.log"
echo "- 学生端启动: ./agent/start_student_agent.sh"
