#!/usr/bin/env python3
"""
AOS Skill 健康度报告
读取 ~/.agents/feedback/ 下的 JSON，生成健康度报告到 ~/.agents/health-report.md
"""

import json
import os
import sys
from pathlib import Path
from datetime import date

# Windows GBK 编码兼容
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

FEEDBACK_DIR = os.path.expanduser("~/.agents/feedback")
REPORT_PATH = os.path.expanduser("~/.agents/health-report.md")


def rate(numerator: int, denominator: int) -> int:
    return round(numerator * 100 / denominator) if denominator else 0


def status_for(useful_rate: int, fm_rate: int) -> str:
    if useful_rate >= 80 and fm_rate >= 70:
        return "✅ 健康"
    if useful_rate < 60 or fm_rate < 50:
        return "⚠️ 关注"
    return "🟡 一般"


def collect_rows(feedback_dir: Path) -> list[dict]:
    rows = []
    if not feedback_dir.exists():
        return rows

    for file in sorted(feedback_dir.glob("*.json")):
        try:
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        s = data.get("stats", {})
        r = data.get("ratings", {})
        calls = s.get("total_calls", 0)
        if calls == 0:
            continue

        useful = r.get("useful", 0)
        fm = s.get("first_match_count", 0)
        rework = s.get("rework_count", 0)

        ur = rate(useful, calls)
        fmr = rate(fm, calls)
        rr = rate(rework, calls)
        st = status_for(ur, fmr)

        rows.append({
            "skill": data.get("skill", file.stem),
            "calls": calls,
            "useful_rate": ur,
            "fm_rate": fmr,
            "rework_rate": rr,
            "status": st,
            "file": file,
            "stats": s,
            "ratings": r,
            "feedback": data.get("feedback", []),
        })

    return rows


def render(rows: list[dict]) -> str:
    today = date.today().isoformat()
    total_calls = sum(r["calls"] for r in rows)
    total_useful = sum(r["ratings"].get("useful", 0) for r in rows)
    total_fm = sum(r["stats"].get("first_match_count", 0) for r in rows) if rows else 0
    total_rework = sum(r["stats"].get("rework_count", 0) for r in rows) if rows else 0

    out = []
    out.append("# AOS Skill 健康度报告")
    out.append("")
    out.append(f"生成时间：{today}")
    out.append("")
    out.append("## 总览")
    out.append("")
    out.append("| 指标 | 数值 |")
    out.append("|------|------|")
    out.append(f"| 已记录 Skill 数 | {len(rows)} |")
    out.append(f"| 总调用次数 | {total_calls} |")
    out.append(f"| 整体有用率 | {rate(total_useful, total_calls)}% |")
    out.append(f"| 整体首次匹配率 | {rate(total_fm, total_calls)}% |")
    out.append(f"| 整体返工率 | {rate(total_rework, total_calls)}% |")
    out.append("")

    if not rows:
        out.append("## 暂无数据")
        out.append("")
        out.append("使用 `aos feedback <skill> --rating ...` 开始记录。")
        return "\n".join(out)

    out.append("## Skill 健康度（按调用次数排序）")
    out.append("")
    out.append("| Skill | 调用 | 有用率 | 首次匹配 | 返工率 | 状态 |")
    out.append("|-------|------|--------|----------|--------|------|")
    for row in sorted(rows, key=lambda r: -r["calls"]):
        out.append(
            f"| {row['skill']} | {row['calls']} | {row['useful_rate']}% | "
            f"{row['fm_rate']}% | {row['rework_rate']}% | {row['status']} |"
        )
    out.append("")

    # 需要关注的 Skill
    out.append("## 需要关注的 Skill")
    out.append("")

    has_warn = False
    for row in rows:
        if row["calls"] < 3:
            continue
        if row["useful_rate"] >= 80 and row["fm_rate"] >= 70:
            continue

        has_warn = True
        out.append(f"### {row['skill']}")
        out.append("")
        out.append(f"- 有用率：{row['useful_rate']}%（调用 {row['calls']} 次）")
        out.append(f"- 首次匹配率：{row['fm_rate']}%")

        if row["fm_rate"] < 50:
            out.append("- ⚠️ 首次匹配率过低：description 可能不够精准或与其他 Skill 边界不清")
        if row["rework_rate"] > 25:
            out.append("- ⚠️ 返工率较高：Skill 输出常需用户二次修改")

        out.append("")
        out.append("**最近反馈：**")
        out.append("")
        for entry in row["feedback"][-5:]:
            note = f": {entry['note']}" if entry.get("note") else ""
            out.append(f"  - [{entry['date']}] {entry['rating']}{note}")

        out.append("")
        out.append("**改进建议：**")
        out.append("")

        if row["fm_rate"] < 50:
            out.append("- 收窄 description 的触发场景")
            out.append("- 加更具体的触发示例")
        if row["rework_rate"] > 25:
            out.append("- 检查 Skill 流程是否覆盖了常见边界场景")
            out.append("- 补充示例与反例")

        mislabeled = row["ratings"].get("mislabeled", 0)
        if mislabeled > 0:
            out.append(f"- {mislabeled} 次「描述不准确」标记：description 需要重新审视")

        outdated = row["ratings"].get("outdated", 0)
        if outdated > 0:
            out.append(f"- {outdated} 次「过时」标记：检查 Skill 内容是否需要更新")

        out.append("")

    if not has_warn:
        out.append("_无。_")
        out.append("")

    out.append("## 长期建议")
    out.append("")
    out.append("- 每季度 review 一次本报告")
    out.append("- 优先改写：高频调用但低有用率的 Skill")
    out.append("- 收集 30+ 反馈后再下结论（避免小样本噪声）")
    out.append("- 持续观察改写后的指标变化")
    out.append("")
    out.append("---")
    out.append("")
    out.append("_本报告由 `scripts/skill-health-report.py` 自动生成。_")
    return "\n".join(out)


def main() -> None:
    feedback_dir = Path(os.environ.get("AOS_FEEDBACK_DIR", FEEDBACK_DIR))
    report_path = Path(os.environ.get("AOS_HEALTH_REPORT", REPORT_PATH))

    if not feedback_dir.exists():
        print(f"📭 反馈目录不存在: {feedback_dir}")
        print("   提示: 用 'aos feedback <skill> --rating ...' 开始记录")
        return

    rows = collect_rows(feedback_dir)
    report = render(rows)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ 健康度报告已生成: {report_path}")
    print()
    print("快速预览：")
    print("---")
    for line in report.split("\n")[:20]:
        print(line)


if __name__ == "__main__":
    main()