#!/usr/bin/env bash
# 使用仓库根目录 .venv，避免 conda base 等环境缺少 langchain_core。
# 用法: ./start.sh              → 默认运行 app_file_uploader.py
#       ./start.sh app_qa.py    → 智能客服
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
APP="${1:-app_qa.py}"
exec "$ROOT/.venv/bin/streamlit" run "$SCRIPT_DIR/$APP"
