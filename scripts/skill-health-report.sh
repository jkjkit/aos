#!/bin/bash
# AOS Skill 健康度报告 (Bash 包装)
# 委托给 skill-health-report.py 跨平台实现

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/skill-health-report.py" "$@"