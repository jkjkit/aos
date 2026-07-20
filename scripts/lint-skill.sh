#!/bin/bash
# AOS 协议 lint 脚本
# 验证 Skill / Workflow / Knowledge / Template 是否符合 ~/.agents/ 规范
# 用法: bash scripts/lint-skill.sh [路径]
#   不传路径：检查整个项目
#   传 skills/<name>：只检查单个 Skill

set -e

AOS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-$AOS_ROOT}"

ERRORS=0
WARNINGS=0

err() { echo "  ❌ $1"; ERRORS=$((ERRORS+1)); }
warn() { echo "  ⚠️  $1"; WARNINGS=$((WARNINGS+1)); }
ok() { echo "  ✅ $1"; }

echo "AOS Lint"
echo "Target: $TARGET"
echo ""

check_skill() {
  local dir="$1"
  local name=$(basename "$dir")
  echo "[Skill] $name"

  # 必须有 SKILL.md
  if [ ! -f "$dir/SKILL.md" ]; then
    err "缺少 SKILL.md"
    return
  fi

  local file="$dir/SKILL.md"

  # 不应该有 README.md
  if [ -f "$dir/README.md" ]; then
    warn "存在 README.md（按规范应为单文件 SKILL.md）"
  fi

  # 不应该有 examples/
  if [ -d "$dir/examples" ]; then
    warn "存在 examples/ 目录（按规范应为单文件 SKILL.md）"
  fi

  # 不应该有 tests/
  if [ -d "$dir/tests" ]; then
    warn "存在 tests/ 目录（按规范应为单文件 SKILL.md）"
  fi

  # frontmatter 必须是 ---
  local first=$(head -1 "$file")
  if [ "$first" != "---" ]; then
    err "第一行不是 ---（缺少 YAML frontmatter）"
    return
  fi

  # frontmatter 必须有 name
  local has_name=$(awk 'NR>1 && /^---$/{exit} NR>1 && /^name:/{print "yes"; exit}' "$file")
  if [ "$has_name" != "yes" ]; then
    err "frontmatter 缺少 name 字段"
  else
    local skill_name=$(awk 'NR>1 && /^---$/{exit} /^name:/{sub(/^name: */,""); print}' "$file")
    if [ "$skill_name" != "$name" ]; then
      err "frontmatter name='$skill_name' 与目录名 '$name' 不一致"
    else
      ok "name 与目录一致"
    fi
  fi

  # frontmatter 必须有 description
  local desc=$(awk 'NR>1 && /^---$/{exit} /^description:/{sub(/^description: */,""); print}' "$file")
  if [ -z "$desc" ]; then
    err "frontmatter 缺少 description 字段"
  else
    local desc_len=${#desc}
    if [ "$desc_len" -lt 10 ]; then
      err "description 过短（${desc_len} 字符，建议 ≥ 10）"
    else
      ok "description: ${desc_len} 字符"
    fi
  fi

  # frontmatter 不应有冗余字段
  local extra_fields=$(awk 'NR>1 && /^---$/{exit} /^[a-z_]+: /{key=$1; gsub(/:.*/,"",key); if(key!="name" && key!="description") print key}' "$file")
  if [ -n "$extra_fields" ]; then
    warn "frontmatter 包含规范外的字段: $extra_fields"
  fi

  # 不应有 # End
  if grep -q "^# End" "$file"; then
    err "包含 # End 标记（应删除）"
  fi

  # 文件大小检查
  local lines=$(wc -l < "$file")
  if [ "$lines" -lt 20 ]; then
    warn "文件仅 ${lines} 行，可能内容不够完整"
  else
    ok "${lines} 行"
  fi

  echo ""
}

check_workflow() {
  local dir="$1"
  local name=$(basename "$dir")
  echo "[Workflow] $name"

  if [ ! -f "$dir/WORKFLOW.md" ]; then
    err "缺少 WORKFLOW.md"
    return
  fi

  local file="$dir/WORKFLOW.md"

  if [ -f "$dir/README.md" ]; then
    warn "存在 README.md（Workflow 按规范应为单文件）"
  fi

  if [ -d "$dir/examples" ]; then
    warn "存在 examples/ 目录（按规范应为单文件）"
  fi

  if grep -q "^# End" "$file"; then
    err "包含 # End 标记"
  fi

  if ! head -1 "$file" | grep -q "^# "; then
    err "第一行不是 # 标题"
  fi

  ok "$(wc -l < "$file") 行"
  echo ""
}

check_knowledge() {
  local dir="$1"
  local name=$(basename "$dir")
  echo "[Knowledge] $name"

  if [ ! -f "$dir/KNOWLEDGE.md" ]; then
    err "缺少 KNOWLEDGE.md"
    return
  fi

  local file="$dir/KNOWLEDGE.md"

  if grep -q "^# End" "$file"; then
    err "包含 # End 标记"
  fi

  ok "$(wc -l < "$file") 行"
  echo ""
}

check_template() {
  local dir="$1"
  local name=$(basename "$dir")
  echo "[Template] $name"

  if [ ! -f "$dir/TEMPLATE.md" ]; then
    err "缺少 TEMPLATE.md"
    return
  fi

  local file="$dir/TEMPLATE.md"

  if grep -q "^# End" "$file"; then
    err "包含 # End 标记"
  fi

  ok "$(wc -l < "$file") 行"
  echo ""
}

# 判断目标类型并执行
if [ -d "$TARGET/skills" ]; then
  # 整个项目
  echo "=== Skills ==="
  for d in "$TARGET/skills"/*/; do
    [ -d "$d" ] && check_skill "$d"
  done

  echo "=== Workflows ==="
  for d in "$TARGET/workflows"/*/; do
    [ -d "$d" ] && check_workflow "$d"
  done

  echo "=== Knowledge ==="
  for d in "$TARGET/knowledge"/*/; do
    [ -d "$d" ] && check_knowledge "$d"
  done

  echo "=== Templates ==="
  for d in "$TARGET/templates"/*/; do
    [ -d "$d" ] && check_template "$d"
  done
elif [ -d "$TARGET" ]; then
  parent=$(basename "$(dirname "$TARGET")")
  case "$parent" in
    skills) check_skill "$TARGET" ;;
    workflows) check_workflow "$TARGET" ;;
    knowledge) check_knowledge "$TARGET" ;;
    templates) check_template "$TARGET" ;;
    *) echo "未知路径：$TARGET"; exit 1 ;;
  esac
fi

echo "=============================="
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo "=============================="

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi