#!/usr/bin/env bash
set -euo pipefail

TARGET_HOST="${1:-}"
TARGET_PORT="${2:-8000}"

if [ -z "${TARGET_HOST}" ]; then
  echo "用法: $0 <教师机IP或域名> [端口，默认8000]"
  exit 1
fi

echo "[连通性测试] 正在测试 ${TARGET_HOST}:${TARGET_PORT} ..."

if command -v nc >/dev/null 2>&1; then
  if nc -z -w 3 "${TARGET_HOST}" "${TARGET_PORT}"; then
    echo "[成功] TCP 端口可达。"
  else
    echo "[失败] TCP 端口不可达，请检查防火墙/安全组。"
    exit 2
  fi
else
  echo "[提示] 未找到 nc，使用 curl 进行 HTTP 探测。"
fi

if curl -sS --max-time 5 "http://${TARGET_HOST}:${TARGET_PORT}/docs" >/dev/null; then
  echo "[成功] HTTP 服务可访问（/docs）。"
else
  echo "[警告] HTTP 未成功响应，可能是服务未启动或路径受限。"
fi
