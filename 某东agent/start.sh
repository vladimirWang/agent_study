#!/usr/bin/env bash
# 使用仓库根目录 .venv，避免 conda base 等环境缺少 langchain_core。
# 启动前加载本目录下的 .env（导出为进程环境变量）。
# 用法: ./start.sh              → 默认运行 app_qa.py
#       ./start.sh app_xxx.py   → 指定应用脚本
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ENV_FILE"
  set +a
fi
APP="${1:-app_qa.py}"
exec "$ROOT/.venv/bin/streamlit" run "$SCRIPT_DIR/$APP"
