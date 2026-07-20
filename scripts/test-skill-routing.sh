#!/bin/bash
# Validate AOS Skill routing regression cases (Bash wrapper)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/test-skill-routing.py" "$@"