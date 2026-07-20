#!/usr/bin/env python3
"""
AOS Feedback CLI (Python)
跨平台实现：Linux / macOS / Windows 都可运行。

用法:
  python3 scripts/aos-feedback.py <skill> [options]

选项:
  --rating <type>         useful | needs-improvement | outdated | mislabeled
  --note "..."            备注
  --context "..."         使用场景
  --first-match           Runtime 首次匹配成功
  --rework                用户返工
  --init                  初始化空反馈文件
  --show                  查看单个 Skill 反馈
  --feedback-dir <path>   自定义反馈目录（默认 ~/.agents/feedback）
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

# Windows GBK 编码兼容
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCHEMA_VERSION = "0.1"
DEFAULT_FEEDBACK_DIR = os.path.expanduser("~/.agents/feedback")
MAX_FEEDBACK_ENTRIES = 50
VALID_RATINGS = {"useful", "needs-improvement", "outdated", "mislabeled"}


def feedback_path(skill: str, base_dir: str) -> Path:
    return Path(base_dir) / f"{skill}.json"


def empty_data(skill: str) -> dict:
    today = date.today().isoformat()
    return {
        "skill": skill,
        "schema_version": SCHEMA_VERSION,
        "created_at": today,
        "updated_at": today,
        "stats": {"total_calls": 0, "first_match_count": 0, "rework_count": 0},
        "ratings": {"useful": 0, "needs-improvement": 0, "outdated": 0, "mislabeled": 0},
        "feedback": [],
    }


def load(skill: str, base_dir: str) -> tuple[dict, Path]:
    path = feedback_path(skill, base_dir)
    if not path.exists():
        return empty_data(skill), path
    with path.open("r", encoding="utf-8") as f:
        return json.load(f), path


def save(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_init(skill: str, base_dir: str) -> None:
    path = feedback_path(skill, base_dir)
    if path.exists():
        print(f"⚠️  已存在: {path}")
        return
    save(empty_data(skill), path)
    print(f"✅ 已初始化: {path}")


def cmd_show(skill: str, base_dir: str) -> None:
    path = feedback_path(skill, base_dir)
    if not path.exists():
        print(f"📭 无反馈数据: {skill}")
        print("   提示: 用 --rating 或 --first-match 开始记录")
        return

    data, _ = load(skill, base_dir)
    s = data["stats"]
    r = data["ratings"]
    total = s["total_calls"]

    useful_rate = round(r["useful"] * 100 / total) if total else 0
    fm_rate = round(s["first_match_count"] * 100 / total) if total else 0
    rework_rate = round(s["rework_count"] * 100 / total) if total else 0

    print(f"📊 反馈数据: {skill}")
    print("---")
    print(f"总调用：{total}")
    print(f"有用率：{useful_rate}%")
    print(f"首次匹配率：{fm_rate}%")
    print(f"返工率：{rework_rate}%")
    print()
    print("评分分布：")
    for k, v in r.items():
        print(f"  {k}: {v}")
    print()
    print("最近反馈（最多 5 条）：")
    recent = data["feedback"][-5:]
    for entry in recent:
        note = f": {entry['note']}" if entry.get("note") else ""
        print(f"  [{entry['date']}] {entry['rating']}{note}")


def cmd_record(skill: str, base_dir: str, rating: str, note: str, context: str) -> None:
    if rating not in VALID_RATINGS:
        print(f"❌ rating 必须是: {', '.join(sorted(VALID_RATINGS))}")
        sys.exit(1)

    data, path = load(skill, base_dir)
    today = date.today().isoformat()

    data["stats"]["total_calls"] += 1
    data["ratings"][rating] += 1
    data["updated_at"] = today

    entry = {"date": today, "rating": rating}
    if note:
        entry["note"] = note
    if context:
        entry["context"] = context
    data["feedback"].append(entry)

    if len(data["feedback"]) > MAX_FEEDBACK_ENTRIES:
        data["feedback"] = data["feedback"][-MAX_FEEDBACK_ENTRIES:]

    save(data, path)
    suffix = f" — {note}" if note else ""
    print(f"✅ 已记录 [{rating}]: {skill}{suffix}")


def cmd_match(skill: str, base_dir: str) -> None:
    data, path = load(skill, base_dir)
    today = date.today().isoformat()
    data["stats"]["total_calls"] += 1
    data["stats"]["first_match_count"] += 1
    data["updated_at"] = today
    save(data, path)
    print(f"✅ 已记录首次匹配: {skill}")


def cmd_rework(skill: str, base_dir: str) -> None:
    data, path = load(skill, base_dir)
    today = date.today().isoformat()
    data["stats"]["total_calls"] += 1
    data["stats"]["rework_count"] += 1
    data["updated_at"] = today
    save(data, path)
    print(f"✅ 已记录返工: {skill}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="aos-feedback",
        description="AOS Feedback CLI - 记录 Skill 使用反馈",
    )
    parser.add_argument("skill", help="Skill 名（kebab-case）")
    parser.add_argument("--rating", choices=sorted(VALID_RATINGS), help="评分")
    parser.add_argument("--note", default="", help="备注")
    parser.add_argument("--context", default="", help="使用场景")
    parser.add_argument("--first-match", action="store_true", help="Runtime 首次匹配成功")
    parser.add_argument("--rework", action="store_true", help="用户返工")
    parser.add_argument("--init", action="store_true", help="初始化空反馈文件")
    parser.add_argument("--show", action="store_true", help="查看反馈")
    parser.add_argument("--feedback-dir", default=DEFAULT_FEEDBACK_DIR, help="反馈目录")

    args = parser.parse_args()

    # 校验 skill 名
    import re
    if not re.match(r"^[a-z][a-z0-9-]*$", args.skill):
        print(f"❌ Skill 名必须是 kebab-case: {args.skill}")
        sys.exit(1)

    base_dir = args.feedback_dir

    if args.init:
        cmd_init(args.skill, base_dir)
    elif args.show:
        cmd_show(args.skill, base_dir)
    elif args.first_match:
        cmd_match(args.skill, base_dir)
    elif args.rework:
        cmd_rework(args.skill, base_dir)
    elif args.rating:
        cmd_record(args.skill, base_dir, args.rating, args.note, args.context)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()