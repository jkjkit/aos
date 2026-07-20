#!/usr/bin/env python3
"""Generate the full AOS manifest and lightweight profile routers."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from skill_profiles import (
    ProfileError,
    collect_available_skills,
    load_profiles,
    validate_profiles,
)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

AOS_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = AOS_ROOT / "MANIFEST.md"
DEFAULT_ROUTER = AOS_ROOT / "ROUTER.md"
ROUTERS_DIR = AOS_ROOT / "routers"
ROLES_FILE = AOS_ROOT / "data" / "skill-roles.json"
ROUTING_FILE = AOS_ROOT / "data" / "skill-routing.json"

ROLE_NAMES = {
    "general": "🌐 通用",
    "dev": "🔧 开发",
    "ops": "⚙️ 运维",
    "data": "📈 数据",
    "design": "🎨 设计",
    "cs": "👥 客服",
    "product": "📊 产品",
    "creative": "✨ 创意",
}


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_roles() -> dict[str, list[str]]:
    data = load_json(ROLES_FILE)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def load_routing() -> dict[str, Any]:
    return load_json(ROUTING_FILE)


def markdown_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def collect_skills() -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for directory in sorted((AOS_ROOT / "skills").iterdir()):
        skill_file = directory / "SKILL.md"
        if not directory.is_dir() or not skill_file.exists():
            continue
        description = ""
        for line in skill_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("description:"):
                description = line[len("description:"):].strip()
                break
        skills.append({
            "name": directory.name,
            "path": f"skills/{directory.name}/SKILL.md",
            "desc": description,
        })
    return skills


def collect_dir(category: str, marker_filename: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for directory in sorted((AOS_ROOT / category).iterdir()):
        if directory.is_dir() and (directory / marker_filename).exists():
            items.append({
                "name": directory.name,
                "path": f"{category}/{directory.name}/{marker_filename}",
            })
    return items


def validate_routing(routing: dict[str, Any], skill_names: set[str]) -> None:
    if not routing:
        return
    errors: list[str] = []
    seen_global: set[str] = set()
    for group_index, group in enumerate(routing.get("groups", []), start=1):
        group_name = group.get("name") or f"group-{group_index}"
        for route in group.get("skills", []):
            name = str(route.get("name", "")).strip()
            if not name:
                errors.append(f"{group_name}: route missing name")
                continue
            if name not in skill_names:
                errors.append(f"{group_name}: unknown Skill '{name}'")
            if name in seen_global:
                errors.append(f"Skill '{name}' is routed more than once")
            seen_global.add(name)
            if not str(route.get("choose_when", "")).strip():
                errors.append(f"{group_name}/{name}: choose_when is required")
            if not str(route.get("avoid_when", "")).strip():
                errors.append(f"{group_name}/{name}: avoid_when is required")
    if errors:
        raise ValueError("Invalid data/skill-routing.json:\n- " + "\n- ".join(errors))


def render_router(
    routing: dict[str, Any],
    profile_name: str,
    active_skills: set[str],
    workflows: list[dict[str, str]],
    today: str,
) -> list[str]:
    lines = [
        "# AOS Router",
        "",
        f"> 自动生成于 {today}；当前 Profile：`{profile_name}`；活动 Skill：{len(active_skills)}。",
        "",
        "仅在 Runtime 提供的 Skill 列表无法唯一匹配时读取本文件。不要默认读取完整 `MANIFEST.md`。",
        "",
        "## 路由原则",
        "",
        "1. 按用户当前要求的最终交付物匹配，不按孤立关键词匹配。",
        "2. 优先选择职责最具体的 Skill；单阶段只加载一个 Skill。",
        "3. 请求明确横跨多个阶段时选择 Workflow。",
        "4. 仍有歧义时对比候选 description；确定后只读取选中的 `SKILL.md`。",
    ]

    for group in routing.get("groups", []):
        routes = [
            route for route in group.get("skills", [])
            if route.get("name") in active_skills
        ]
        if not routes:
            continue
        lines.extend(["", f"## {group['name']}", ""])
        for route in routes:
            lines.append(
                f"- `{markdown_cell(route['name'])}`："
                f"{markdown_cell(route['choose_when'])}"
            )

    lines.extend(["", "## Workflows", ""])
    workflow_labels = {
        "new-feature": "需求到实现与验证的完整新功能流程",
        "bug-fix": "复现、定位、修复和回归的完整故障流程",
        "code-review": "自动检查、人工审查、修改确认和合并验证",
        "deployment": "部署前检查、发布、健康检查、烟测和回滚准备",
        "release": "版本号、变更日志、验证、发布、部署和反馈监控",
    }
    for workflow in workflows:
        lines.append(
            f"- `{workflow['name']}`："
            f"{workflow_labels.get(workflow['name'], '编排多个 Skill 的多阶段流程')}"
        )
    return lines


def render_skills_by_role(skills: list[dict[str, str]], roles: dict[str, list[str]]) -> list[str]:
    role_to_skills: dict[str, list[str]] = {}
    for skill in skills:
        for role in roles.get(skill["name"], []):
            role_to_skills.setdefault(role, []).append(skill["name"])

    lines = [
        "## Skill 岗位索引",
        "",
        "岗位只用于浏览和发现；Runtime 路由应优先使用轻量 `ROUTER.md`。",
        "",
        "| Role | Skills |",
        "|---|---|",
    ]
    for role_key, role_label in ROLE_NAMES.items():
        names = role_to_skills.get(role_key, [])
        if names:
            lines.append(f"| {role_label} | {', '.join(f'`{name}`' for name in names)} |")

    uncategorized = [skill["name"] for skill in skills if not roles.get(skill["name"])]
    if uncategorized:
        lines.append(f"| — | {', '.join(f'`{name}`' for name in uncategorized)} |")
    return lines


def render_skills_alphabetical(
    skills: list[dict[str, str]], roles: dict[str, list[str]]
) -> list[str]:
    lines = [
        "## Skills（按字母顺序）",
        "",
        "| Name | 适用岗位 | 路径 | 用途 |",
        "|---|---|---|---|",
    ]
    for skill in skills:
        role_text = ", ".join(roles.get(skill["name"], [])) or "—"
        lines.append(
            f"| {skill['name']} | {role_text} | {skill['path']} | {skill['desc']} |"
        )
    return lines


def render_section(title: str, headers: list[str], items: list[dict[str, str]]) -> list[str]:
    lines = [f"## {title}", "", "| " + " | ".join(headers) + " |"]
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for item in items:
        lines.append("| " + " | ".join(str(item.get(header, "")) for header in headers) + " |")
    return lines


def build_manifest(
    output: Path,
    skills: list[dict[str, str]],
    roles: dict[str, list[str]],
    workflows: list[dict[str, str]],
    knowledge: list[dict[str, str]],
    templates: list[dict[str, str]],
    today: str,
) -> None:
    lines = [
        "# AOS Manifest",
        "",
        "完整能力目录，用于发现和维护；Runtime 日常匹配请使用轻量 `ROUTER.md`。",
        "",
        f"> 自动生成于 {today}。修改源数据后重新运行 `python3 scripts/build-manifest.py`。",
        "",
    ]
    lines.extend(render_skills_by_role(skills, roles))
    lines.extend(["", "> 通用 Skill 可被任何岗位使用；岗位标签不是最终路由依据。", ""])
    lines.extend(render_skills_alphabetical(skills, roles))
    lines.append("")
    lines.extend(render_section(
        "Workflows",
        ["Name", "路径", "触发场景"],
        [
            {"Name": item["name"], "路径": item["path"], "触发场景": "编排多个 Skill"}
            for item in workflows
        ],
    ))
    lines.append("")
    lines.extend(render_section(
        "Knowledge",
        ["Name", "路径", "领域"],
        [
            {"Name": item["name"], "路径": item["path"], "领域": "被动参考"}
            for item in knowledge
        ],
    ))
    lines.append("")
    lines.extend(render_section(
        "Templates",
        ["Name", "路径", "输出类型"],
        [
            {"Name": item["name"], "路径": item["path"], "输出类型": "文档模板"}
            for item in templates
        ],
    ))
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    try:
        roles = load_roles()
        routing = load_routing()
        skills = collect_skills()
        skill_names = {skill["name"] for skill in skills}
        validate_routing(routing, skill_names)

        profile_data = load_profiles()
        resolved_profiles = validate_profiles(
            profile_data,
            collect_available_skills(),
        )
        workflows = collect_dir("workflows", "WORKFLOW.md")
        knowledge = collect_dir("knowledge", "KNOWLEDGE.md")
        templates = collect_dir("templates", "TEMPLATE.md")
        today = datetime.now().strftime("%Y-%m-%d")

        build_manifest(output, skills, roles, workflows, knowledge, templates, today)

        ROUTERS_DIR.mkdir(parents=True, exist_ok=True)
        for profile_name, active in resolved_profiles.items():
            router_lines = render_router(
                routing,
                profile_name,
                set(active),
                workflows,
                today,
            )
            (ROUTERS_DIR / f"{profile_name}.md").write_text(
                "\n".join(router_lines) + "\n",
                encoding="utf-8",
            )

        default_profile = profile_data["default_profile"]
        DEFAULT_ROUTER.write_text(
            (ROUTERS_DIR / f"{default_profile}.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        print(f"MANIFEST 已生成：{output}")
        print(f"ROUTER 已生成：{DEFAULT_ROUTER} ({default_profile})")
        print(f"  Skills:     {len(skills)}")
        print(f"  Profiles:   {len(resolved_profiles)}")
        print(f"  Workflows:  {len(workflows)}")
        print(f"  Knowledge:  {len(knowledge)}")
        print(f"  Templates:  {len(templates)}")
        return 0
    except (OSError, ValueError, ProfileError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
