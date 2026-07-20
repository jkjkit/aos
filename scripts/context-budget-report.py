#!/usr/bin/env python3
"""Report and enforce AOS progressive-loading context budgets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from skill_profiles import collect_available_skills, load_profiles, validate_profiles

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

AOS_ROOT = Path(__file__).resolve().parent.parent
BUDGET_FILE = AOS_ROOT / "data" / "context-budgets.json"
RUNTIME_DIR = AOS_ROOT / "runtimes"
ROUTERS_DIR = AOS_ROOT / "routers"
MANIFEST_FILE = AOS_ROOT / "MANIFEST.md"
SKILLS_DIR = AOS_ROOT / "skills"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def file_bytes(path: Path) -> int:
    return path.stat().st_size if path.exists() else -1


def skill_metadata(name: str) -> tuple[int, str]:
    path = SKILLS_DIR / name / "SKILL.md"
    text = path.read_text(encoding="utf-8-sig")
    description = ""
    for line in text.splitlines():
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip()
            break
    return path.stat().st_size, description


def format_bytes(value: int) -> str:
    if value < 0:
        return "missing"
    if value < 1024:
        return f"{value} B"
    return f"{value / 1024:.1f} KiB"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 when a hard context budget is exceeded or a required file is missing",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        limits = load_json(BUDGET_FILE)["limits"]
        profile_data = load_profiles()
        profiles = validate_profiles(profile_data, collect_available_skills())
    except (OSError, KeyError, json.JSONDecodeError, ValueError) as exc:
        print(f"[ERROR] unable to load context budget data: {exc}", file=sys.stderr)
        return 1

    default_profile = profile_data["default_profile"]
    skill_info = {name: skill_metadata(name) for name in collect_available_skills()}
    hard_errors: list[str] = []
    warnings: list[str] = []

    print("AOS context budget report")
    print(f"  Default profile: {default_profile}")
    print(f"  Manifest:        {format_bytes(file_bytes(MANIFEST_FILE))}")

    print("\nRuntime entries:")
    for path in sorted(RUNTIME_DIR.glob("*.md")):
        size = file_bytes(path)
        status = "OK" if 0 <= size <= limits["runtime_entry_bytes"] else "ERROR"
        print(
            f"  {path.name:<12} {format_bytes(size):>10} / "
            f"{format_bytes(limits['runtime_entry_bytes']):>8}  {status}"
        )
        if status == "ERROR":
            hard_errors.append(
                f"{path.relative_to(AOS_ROOT)} is {size} bytes; "
                f"limit is {limits['runtime_entry_bytes']}"
            )

    print("\nProfiles:")
    for name, active in sorted(profiles.items()):
        router = ROUTERS_DIR / f"{name}.md"
        router_size = file_bytes(router)
        description_chars = sum(len(skill_info[skill][1]) for skill in active)
        total_skill_bytes = sum(skill_info[skill][0] for skill in active)
        print(
            f"  {name:<8} skills={len(active):>2}  router={format_bytes(router_size):>9}  "
            f"descriptions={description_chars:>4} chars  skill-md={format_bytes(total_skill_bytes)}"
        )
        if router_size < 0:
            hard_errors.append(f"missing router: {router.relative_to(AOS_ROOT)}")

    default_active = profiles[default_profile]
    default_router = ROUTERS_DIR / f"{default_profile}.md"
    default_description_chars = sum(
        len(skill_info[name][1]) for name in default_active
    )
    if file_bytes(default_router) > limits["default_router_bytes"]:
        hard_errors.append(
            f"default router is {file_bytes(default_router)} bytes; "
            f"limit is {limits['default_router_bytes']}"
        )
    if len(default_active) > limits["default_active_skills"]:
        hard_errors.append(
            f"default profile has {len(default_active)} Skills; "
            f"limit is {limits['default_active_skills']}"
        )
    if default_description_chars > limits["default_description_chars"]:
        hard_errors.append(
            f"default profile descriptions total {default_description_chars} chars; "
            f"limit is {limits['default_description_chars']}"
        )

    sizes = [size for size, _ in skill_info.values()]
    largest_name = max(skill_info, key=lambda item: skill_info[item][0])
    print("\nSkill files:")
    print(f"  Count:   {len(sizes)}")
    print(f"  Total:   {format_bytes(sum(sizes))}")
    print(f"  Average: {format_bytes(round(sum(sizes) / len(sizes)))}")
    print(
        f"  Largest: {largest_name} ({format_bytes(skill_info[largest_name][0])})"
    )
    for name, (size, _) in sorted(skill_info.items()):
        if size > limits["skill_md_error_bytes"]:
            hard_errors.append(
                f"skills/{name}/SKILL.md is {size} bytes; "
                f"hard limit is {limits['skill_md_error_bytes']}"
            )
        elif size > limits["skill_md_warning_bytes"]:
            warnings.append(
                f"skills/{name}/SKILL.md is {size} bytes; "
                f"warning threshold is {limits['skill_md_warning_bytes']}"
            )

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")
    if hard_errors:
        print("\nBudget failures:")
        for error in hard_errors:
            print(f"  - {error}")
        return 1 if args.check else 0

    print("\nContext budget passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())