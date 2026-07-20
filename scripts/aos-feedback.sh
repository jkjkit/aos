#!/bin/bash
# AOS Feedback CLI (Bash 包装)
# 委托给 aos-feedback.py 跨平台实现

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/aos-feedback.py" "$@"