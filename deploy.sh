#!/bin/bash
# AOS 一键部署脚本 (macOS / Linux / Git Bash)
# 用法: bash deploy.sh [core|ai|design|full] [isolate|keep|restore]

set -euo pipefail

PROFILE="${1:-core}"
THIRD_PARTY="${2:-isolate}"
AOS_SOURCE="$(cd "$(dirname "$0")" && pwd -P)"
AOS_TARGET="${AOS_TARGET:-$HOME/.agents}"
AOS_INSTALL_RUNTIME="${AOS_INSTALL_RUNTIME:-0}"
# Backward-compatible no-op. Runtime entry files are no longer installed by default.
AOS_SKIP_RUNTIME="${AOS_SKIP_RUNTIME:-0}"

case "$PROFILE" in core|ai|design|full) ;; *) echo "[ERROR] invalid profile: $PROFILE" >&2; exit 2 ;; esac
case "$THIRD_PARTY" in isolate|keep|restore) ;; *) echo "[ERROR] invalid third-party policy: $THIRD_PARTY" >&2; exit 2 ;; esac

mkdir -p "$AOS_TARGET"
AOS_TARGET="$(cd "$AOS_TARGET" && pwd -P)"
if [ "$AOS_TARGET" = "/" ]; then
  echo "[ERROR] refusing to deploy to filesystem root" >&2
  exit 2
fi

safe_child() {
  case "$1/" in
    "$2"/*) ;;
    *) echo "[ERROR] unsafe path outside managed root: $1 (root: $2)" >&2; exit 2 ;;
  esac
}

safe_remove_dir() {
  safe_child "$1" "$2"
  [ ! -e "$1" ] || rm -rf -- "$1"
}

PROFILE_FILE="$(mktemp)"
ALL_FILE="$(mktemp)"
cleanup() { rm -f -- "$PROFILE_FILE" "$ALL_FILE"; }
trap cleanup EXIT

printf '\n  AOS - Agent Operating System\n'
printf '  Profile: %s\n' "$PROFILE"
printf '  Third-party policy: %s\n' "$THIRD_PARTY"
printf '  Deploy to: %s\n' "$AOS_TARGET"
if [ "$AOS_INSTALL_RUNTIME" = "1" ] && [ "$AOS_SKIP_RUNTIME" != "1" ]; then
  printf '  Runtime entry files: install on request\n'
else
  printf '  Runtime entry files: not modified by default\n'
fi
if [ "$AOS_SKIP_RUNTIME" = "1" ]; then
  printf '  [WARN] AOS_SKIP_RUNTIME is retained for compatibility; Runtime entry files are not installed unless AOS_INSTALL_RUNTIME=1.\n' >&2
fi
printf '\n' 

python3 "$AOS_SOURCE/scripts/build-manifest.py"
python3 "$AOS_SOURCE/scripts/skill_profiles.py" --profile "$PROFILE" --format lines > "$PROFILE_FILE"
python3 "$AOS_SOURCE/scripts/skill_profiles.py" --all --format lines > "$ALL_FILE"

mkdir -p "$AOS_TARGET/feedback"

# 1. 部署核心目录。
for dir in protocols workflows templates knowledge; do
  echo "  [$dir] deploying..."
  safe_remove_dir "$AOS_TARGET/$dir" "$AOS_TARGET"
  cp -R "$AOS_SOURCE/$dir" "$AOS_TARGET/$dir"
done

# 2. 按 Profile 部署 Skills，并处理第三方 Skill。
echo "  [skills] deploying profile '$PROFILE'..."
SKILLS_TARGET="$AOS_TARGET/skills"
PACK_SKILLS_TARGET="$AOS_TARGET/packs/third-party/skills"
mkdir -p "$SKILLS_TARGET" "$PACK_SKILLS_TARGET"

if [ "$THIRD_PARTY" = "restore" ]; then
  for skill_dir in "$PACK_SKILLS_TARGET"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    dest="$SKILLS_TARGET/$skill_name"
    safe_child "${skill_dir%/}" "$PACK_SKILLS_TARGET"
    safe_child "$dest" "$SKILLS_TARGET"
    if [ -e "$dest" ]; then
      echo "  [WARN] cannot restore '$skill_name': active destination exists" >&2
    else
      mv -- "${skill_dir%/}" "$dest"
      echo "    restored third-party: $skill_name"
    fi
  done
fi

if [ "$THIRD_PARTY" = "isolate" ]; then
  for skill_dir in "$SKILLS_TARGET"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    if ! grep -Fqx -- "$skill_name" "$ALL_FILE"; then
      dest="$PACK_SKILLS_TARGET/$skill_name"
      safe_child "${skill_dir%/}" "$SKILLS_TARGET"
      safe_child "$dest" "$PACK_SKILLS_TARGET"
      if [ -e "$dest" ]; then
        echo "  [WARN] cannot isolate '$skill_name': pack destination exists; leaving active" >&2
      else
        mv -- "${skill_dir%/}" "$dest"
        echo "    isolated third-party: $skill_name"
      fi
    fi
  done
fi

while IFS= read -r skill_name; do
  [ -n "$skill_name" ] || continue
  if ! grep -Fqx -- "$skill_name" "$PROFILE_FILE"; then
    safe_remove_dir "$SKILLS_TARGET/$skill_name" "$SKILLS_TARGET"
  fi
done < "$ALL_FILE"

while IFS= read -r skill_name; do
  [ -n "$skill_name" ] || continue
  dest="$SKILLS_TARGET/$skill_name"
  safe_remove_dir "$dest" "$SKILLS_TARGET"
  cp -R "$AOS_SOURCE/skills/$skill_name" "$dest"
  echo "    + $skill_name"
done < "$PROFILE_FILE"

# 3. 部署 Router、Manifest 和托管状态。
cp "$AOS_SOURCE/routers/$PROFILE.md" "$AOS_TARGET/ROUTER.md"
cp "$AOS_SOURCE/MANIFEST.md" "$AOS_TARGET/MANIFEST.md"
python3 "$AOS_SOURCE/scripts/skill_profiles.py" \
  --profile "$PROFILE" \
  --write-state "$AOS_TARGET/.aos-managed-skills.json" \
  --third-party-policy "$THIRD_PARTY" >/dev/null

# 4. 安装 Runtime 入口文件。
# Default behavior preserves user-owned Runtime files.
if [ "$AOS_INSTALL_RUNTIME" = "1" ] && [ "$AOS_SKIP_RUNTIME" != "1" ]; then
  echo ""
  echo "  [runtime] installing entry files..."
  mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.cursor/rules"
  cp "$AOS_SOURCE/runtimes/claude.md" "$HOME/.claude/CLAUDE.md"
  cp "$AOS_SOURCE/runtimes/codex.md" "$HOME/.codex/AGENT.md"
  cp "$AOS_SOURCE/runtimes/cursor.md" "$HOME/.cursor/rules/aos.md"
  echo "    + ~/.claude/CLAUDE.md"
  echo "    + ~/.codex/AGENT.md"
  echo "    + ~/.cursor/rules/aos.md"
fi

# 5. 部署观察层脚本。
echo ""
echo "  [scripts] installing observation tools..."
mkdir -p "$AOS_TARGET/scripts"
for file in aos-feedback.py aos-feedback.sh skill-health-report.py skill-health-report.sh; do
  cp "$AOS_SOURCE/scripts/$file" "$AOS_TARGET/scripts/$file"
done
chmod +x "$AOS_TARGET/scripts/"*.sh "$AOS_TARGET/scripts/"*.py

ACTIVE_COUNT="$(wc -l < "$PROFILE_FILE" | tr -d ' ')"
printf '\n  Done! Active AOS Skills: %s; profile: %s.\n\n' "$ACTIVE_COUNT" "$PROFILE"