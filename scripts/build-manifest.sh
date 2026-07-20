#!/bin/bash
# AOS MANIFEST 自动生成脚本 (Bash 包装)
# 委托给 build-manifest.py 跨平台实现

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/build-manifest.py" "$@"