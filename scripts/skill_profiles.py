#!/usr/bin/env python3
"""Resolve and validate AOS Skill deployment profiles."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

AOS_ROOT = Path(__file__).resolve().parent.parent
PROFILES_FILE = AOS_ROOT / "data" / "skill-profiles.json"
SKILLS_DIR = AOS_ROOT / "skills"


class ProfileError(Exception):
    pass


def load_profiles(path: Path = PROFILES_FILE) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ProfileError(f"missing profile file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ProfileError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(data.get("profiles"), dict) or not data["profiles"]:
        raise ProfileError("skill-profiles.json must contain a non-empty profiles object")
    return data


def collect_available_skills(root: Path = SKILLS_DIR) -> set[str]:
    if not root.exists():
        raise ProfileError(f"missing skills directory: {root}")
    return {
        child.name
        for child in root.iterdir()
        if child.is_dir() and (child / "SKILL.md").exists()
    }


def resolve_profile(
    name: str,
    data: dict[str, Any],
    available: set[str],
    stack: tuple[str, ...] = (),
) -> list[str]:
    profiles = data["profiles"]
    if name not in profiles:
        raise ProfileError(
            f"unknown profile '{name}'; available: {', '.join(sorted(profiles))}"
        )
    if name in stack:
        chain = " -> ".join((*stack, name))
        raise ProfileError(f"profile inheritance cycle: {chain}")

    profile = profiles[name]
    if not isinstance(profile, dict):
        raise ProfileError(f"profile '{name}' must be an object")

    selected: set[str] = set()
    if profile.get("include_all") is True:
        selected.update(available)

    extends = profile.get("extends", [])
    if not isinstance(extends, list):
        raise ProfileError(f"profile '{name}'.extends must be an array")
    for parent in extends:
        if not isinstance(parent, str) or not parent.strip():
            raise ProfileError(f"profile '{name}'.extends contains an invalid name")
        selected.update(resolve_profile(parent.strip(), data, available, (*stack, name)))

    skills = profile.get("skills", [])
    if not isinstance(skills, list):
        raise ProfileError(f"profile '{name}'.skills must be an array")
    for skill in skills:
        if not isinstance(skill, str) or not skill.strip():
            raise ProfileError(f"profile '{name}'.skills contains an invalid name")
        selected.add(skill.strip())

    unknown = sorted(selected - available)
    if unknown:
        raise ProfileError(
            f"profile '{name}' references unknown Skills: {', '.join(unknown)}"
        )
    return sorted(selected)


def validate_profiles(data: dict[str, Any], available: set[str]) -> dict[str, list[str]]:
    default = str(data.get("default_profile", "")).strip()
    if not default:
        raise ProfileError("skill-profiles.json is missing default_profile")
    if default not in data["profiles"]:
        raise ProfileError(f"default profile '{default}' does not exist")

    resolved = {
        name: resolve_profile(name, data, available)
        for name in sorted(data["profiles"])
    }
    full_profiles = [
        name for name, profile in data["profiles"].items()
        if isinstance(profile, dict) and profile.get("include_all") is True
    ]
    for name in full_profiles:
        if set(resolved[name]) != available:
            raise ProfileError(f"include_all profile '{name}' did not resolve all Skills")
    return resolved


def write_state(
    path: Path,
    profile: str,
    active_skills: list[str],
    third_party_policy: str,
) -> None:
    payload = {
        "version": 1,
        "profile": profile,
        "third_party_policy": third_party_policy,
        "active_skills": active_skills,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", help="Profile name to resolve")
    parser.add_argument(
        "--format",
        choices=("lines", "json"),
        default="lines",
        help="Output format for resolved Skills",
    )
    parser.add_argument("--all", action="store_true", help="Output all repository Skills")
    parser.add_argument("--list", action="store_true", help="List profile names and sizes")
    parser.add_argument("--write-state", type=Path, help="Write deployment managed state JSON")
    parser.add_argument(
        "--third-party-policy",
        choices=("isolate", "keep", "restore"),
        default="isolate",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = load_profiles()
        available = collect_available_skills()
        resolved = validate_profiles(data, available)

        if args.list:
            for name in sorted(resolved):
                marker = " (default)" if name == data["default_profile"] else ""
                description = data["profiles"][name].get("description", "")
                print(f"{name}{marker}: {len(resolved[name])} Skills - {description}")
            return 0

        if args.all:
            skills = sorted(available)
            profile_name = "all"
        else:
            profile_name = args.profile or data["default_profile"]
            if profile_name not in resolved:
                raise ProfileError(f"unknown profile '{profile_name}'")
            skills = resolved[profile_name]

        if args.write_state:
            if profile_name == "all":
                raise ProfileError("--write-state requires a named profile, not --all")
            write_state(
                args.write_state,
                profile_name,
                skills,
                args.third_party_policy,
            )

        if args.format == "json":
            print(json.dumps(skills, ensure_ascii=False))
        else:
            for skill in skills:
                print(skill)
        return 0
    except ProfileError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
