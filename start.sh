#!/usr/bin/env bash
# 一键构建前端并启动 Flask（单端口）
set -e
cd "$(dirname "$0")"

PY="${PYTHON:-python}"

if ! "$PY" -c "import flask" >/dev/null 2>&1; then
  echo "[ERROR] 当前解释器未安装 Flask：$PY"
  echo "        请执行：pip install -r backend/requirements.txt"
  echo "        或指定解释器：PYTHON=/path/to/python ./start.sh"
  exit 1
fi

cd frontend
if [ ! -d node_modules ]; then
  echo "→ 安装前端依赖…"
  npm install
fi
if [ ! -f dist/index.html ]; then
  echo "→ 构建前端…"
  npm run build
else
  echo "→ 检测到已有构建产物，跳过构建"
fi

cd ../backend
echo "→ 启动服务：http://127.0.0.1:${PORT:-5000}"
exec "$PY" app.py
