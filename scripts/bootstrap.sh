#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

check_command() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERROR] 缺少依赖命令: $cmd"
    exit 1
  fi
}

echo "[1/4] 检查基础命令..."
check_command docker
check_command python3
check_command node
check_command npm

echo "[2/4] 创建 Python 虚拟环境..."
cd "$ROOT_DIR"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip

echo "[3/4] 安装后端依赖..."
pip install -r backend/requirements.txt

echo "[4/4] 安装前端依赖..."
cd "$ROOT_DIR/frontend"
npm install

cat <<'EOF'

✅ 依赖安装完成。可按以下步骤启动：

1) 复制环境变量模板
   cp .env.example .env

2) 启动 Docker（Postgres + Backend + Frontend）
   docker compose up -d --build

3) 查看服务状态
   docker compose ps

4) 本地开发模式（可选）
   # 后端
   cd backend && uvicorn app.main:app --reload --port 8000

   # 前端（另开终端）
   cd frontend && npm run dev
EOF
