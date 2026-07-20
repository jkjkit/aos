#!/usr/bin/env python3
"""Validate and score AOS Skill routing regression cases.

Static mode validates that the regression corpus, routing data, installed Skills,
Workflows, and generated MANIFEST stay in sync.

Prediction mode compares decisions produced by a Runtime with the expected route:

    python scripts/test-skill-routing.py --predictions predictions.json

Prediction files may be either an object mapping case IDs to names, or a list of
objects containing ``id`` plus ``prediction``/``name``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

AOS_ROOT = Path(__file__).resolve().parent.parent
CASES_FILE = AOS_ROOT / "tests" / "skill-routing" / "cases.json"
ROUTING_FILE = AOS_ROOT / "data" / "skill-routing.json"
MANIFEST_FILE = AOS_ROOT / "MANIFEST.md"
ROUTER_FILE = AOS_ROOT / "ROUTER.md"
ROUTERS_DIR = AOS_ROOT / "routers"
SKILLS_DIR = AOS_ROOT / "skills"
WORKFLOWS_DIR = AOS_ROOT / "workflows"
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class ValidationError(Exception):
    """Raised when the routing contract or regression corpus is invalid."""


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(AOS_ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> Any:
    label = display_path(path)
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {label}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"invalid JSON in {label}: "
            f"line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def collect_named_dirs(parent: Path, marker: str) -> set[str]:
    if not parent.exists():
        raise ValidationError(f"missing directory: {parent.relative_to(AOS_ROOT)}")
    return {
        child.name
        for child in parent.iterdir()
        if child.is_dir() and (child / marker).exists()
    }


def normalize_input(value: str) -> str:
    return " ".join(value.split()).casefold()


def build_routing_index(routing: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]]]:
    groups = routing.get("groups")
    if not isinstance(groups, list) or not groups:
        raise ValidationError("data/skill-routing.json must contain a non-empty groups array")

    route_index: dict[str, dict[str, Any]] = {}
    group_members: dict[str, set[str]] = {}
    errors: list[str] = []

    for group_number, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            errors.append(f"routing group #{group_number} must be an object")
            continue
        group_name = str(group.get("name", "")).strip()
        if not group_name:
            errors.append(f"routing group #{group_number} is missing name")
            group_name = f"group-{group_number}"
        routes = group.get("skills")
        if not isinstance(routes, list) or not routes:
            errors.append(f"routing group '{group_name}' must contain skills")
            continue

        members: set[str] = set()
        for route_number, route in enumerate(routes, start=1):
            if not isinstance(route, dict):
                errors.append(f"{group_name}: route #{route_number} must be an object")
                continue
            name = str(route.get("name", "")).strip()
            if not name:
                errors.append(f"{group_name}: route #{route_number} is missing name")
                continue
            if name in route_index:
                errors.append(
                    f"skill '{name}' is routed more than once: "
                    f"'{route_index[name]['group']}' and '{group_name}'"
                )
            if not str(route.get("choose_when", "")).strip():
                errors.append(f"{group_name}/{name}: choose_when is required")
            if not str(route.get("avoid_when", "")).strip():
                errors.append(f"{group_name}/{name}: avoid_when is required")
            route_index[name] = {**route, "group": group_name}
            members.add(name)
        group_members[group_name] = members

    if errors:
        raise ValidationError("invalid routing data:\n- " + "\n- ".join(errors))
    return route_index, group_members


def validate_manifest(skills: set[str]) -> list[str]:
    errors: list[str] = []
    if not MANIFEST_FILE.exists():
        return ["MANIFEST.md is missing; run scripts/build-manifest.py"]

    manifest = MANIFEST_FILE.read_text(encoding="utf-8")
    if "## 快速匹配规则" in manifest:
        errors.append("MANIFEST.md still contains the legacy quick routing section")
    if "Runtime 日常匹配请使用轻量 `ROUTER.md`" not in manifest:
        errors.append("MANIFEST.md does not identify ROUTER.md as the Runtime entry")

    for name in sorted(skills):
        row_marker = f"| {name} |"
        path_marker = f"skills/{name}/SKILL.md"
        if row_marker not in manifest or path_marker not in manifest:
            errors.append(
                f"MANIFEST.md is missing Skill '{name}'; run scripts/build-manifest.py"
            )
    return errors


def validate_routers(
    route_index: dict[str, dict[str, Any]],
    routing: dict[str, Any],
    skills: set[str],
    workflows: set[str],
) -> list[str]:
    errors: list[str] = []
    try:
        from skill_profiles import collect_available_skills, load_profiles, validate_profiles

        profile_data = load_profiles()
        resolved = validate_profiles(profile_data, collect_available_skills())
    except Exception as exc:
        return [f"unable to validate Skill profiles: {exc}"]

    default_profile = profile_data["default_profile"]
    default_router = ROUTERS_DIR / f"{default_profile}.md"
    if not ROUTER_FILE.exists():
        errors.append("ROUTER.md is missing; run scripts/build-manifest.py")
    if not default_router.exists():
        errors.append(
            f"default profile router '{display_path(default_router)}' is missing"
        )
    if ROUTER_FILE.exists() and default_router.exists():
        if ROUTER_FILE.read_bytes() != default_router.read_bytes():
            errors.append(
                f"ROUTER.md must exactly match the default '{default_profile}' profile router"
            )

    route_names = set(route_index)
    if not route_names <= skills:
        missing = ", ".join(sorted(route_names - skills))
        errors.append(f"routers reference missing Skills: {missing}")

    for profile_name, active_names in sorted(resolved.items()):
        router_path = ROUTERS_DIR / f"{profile_name}.md"
        if not router_path.exists():
            errors.append(
                f"profile router '{display_path(router_path)}' is missing; "
                "run scripts/build-manifest.py"
            )
            continue
        router = router_path.read_text(encoding="utf-8")
        active = set(active_names)
        expected_header = f"当前 Profile：`{profile_name}`；活动 Skill：{len(active)}。"
        if expected_header not in router:
            errors.append(f"{display_path(router_path)} has an invalid profile header")

        for name, route in route_index.items():
            line = f"- `{name}`：{route['choose_when']}"
            if name in active and line not in router:
                errors.append(
                    f"{display_path(router_path)} is missing routed Skill '{name}'"
                )
            if name not in active and line in router:
                errors.append(
                    f"{display_path(router_path)} contains inactive Skill '{name}'"
                )

        for group in routing.get("groups", []):
            group_name = str(group.get("name", "")).strip()
            group_active = any(
                str(route.get("name", "")).strip() in active
                for route in group.get("skills", [])
            )
            heading = f"## {group_name}"
            if group_name and group_active and heading not in router:
                errors.append(
                    f"{display_path(router_path)} is missing routing group '{group_name}'"
                )

        for workflow in workflows:
            if f"- `{workflow}`：" not in router:
                errors.append(
                    f"{display_path(router_path)} is missing Workflow '{workflow}'"
                )

    full_router = ROUTERS_DIR / "full.md"
    if full_router.exists():
        full_text = full_router.read_text(encoding="utf-8")
        for name, route in route_index.items():
            if f"- `{name}`：{route['choose_when']}" not in full_text:
                errors.append(f"routers/full.md is missing routed Skill '{name}'")
    return errors


def validate_cases(
    corpus: dict[str, Any],
    routing: dict[str, Any],
    skills: set[str],
    workflows: set[str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    errors: list[str] = []
    route_index, group_members = build_routing_index(routing)

    version = corpus.get("version")
    if not isinstance(version, int) or version < 1:
        errors.append("cases.json version must be a positive integer")

    minimum = corpus.get("minimum_cases_per_routed_skill", 2)
    if not isinstance(minimum, int) or minimum < 1:
        errors.append("minimum_cases_per_routed_skill must be a positive integer")
        minimum = 2

    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases.json must contain a non-empty cases array")
        cases = []

    missing_skills = sorted(set(route_index) - skills)
    if missing_skills:
        errors.append("routing references missing Skills: " + ", ".join(missing_skills))

    seen_ids: set[str] = set()
    seen_inputs: dict[str, str] = {}
    skill_coverage: Counter[str] = Counter()
    workflow_coverage: Counter[str] = Counter()
    group_coverage: Counter[str] = Counter()

    for position, case in enumerate(cases, start=1):
        label = f"case #{position}"
        if not isinstance(case, dict):
            errors.append(f"{label} must be an object")
            continue

        case_id = str(case.get("id", "")).strip()
        if not case_id:
            errors.append(f"{label} is missing id")
        elif not ID_PATTERN.fullmatch(case_id):
            errors.append(f"{case_id}: id must match {ID_PATTERN.pattern}")
        elif case_id in seen_ids:
            errors.append(f"duplicate case id: {case_id}")
        else:
            seen_ids.add(case_id)
        label = case_id or label

        user_input = str(case.get("input", "")).strip()
        if not user_input:
            errors.append(f"{label}: input is required")
        else:
            normalized = normalize_input(user_input)
            previous = seen_inputs.get(normalized)
            if previous:
                errors.append(f"{label}: duplicate input already used by {previous}")
            else:
                seen_inputs[normalized] = label

        reason = str(case.get("reason", "")).strip()
        if not reason:
            errors.append(f"{label}: reason is required")

        expected = case.get("expected")
        if not isinstance(expected, dict):
            errors.append(f"{label}: expected must be an object")
            continue
        kind = str(expected.get("kind", "")).strip()
        name = str(expected.get("name", "")).strip()
        if kind not in {"skill", "workflow"}:
            errors.append(f"{label}: expected.kind must be 'skill' or 'workflow'")
            continue
        known_names = skills if kind == "skill" else workflows
        if name not in known_names:
            errors.append(f"{label}: unknown expected {kind} '{name}'")

        confusable = case.get("confusable_with")
        if not isinstance(confusable, list) or not confusable:
            errors.append(f"{label}: confusable_with must be a non-empty array")
            confusable = []
        clean_confusable: list[str] = []
        for candidate in confusable:
            candidate_name = str(candidate).strip()
            if not candidate_name:
                errors.append(f"{label}: confusable_with contains an empty name")
                continue
            if candidate_name not in skills and candidate_name not in workflows:
                errors.append(f"{label}: unknown confusable target '{candidate_name}'")
            if candidate_name == name:
                errors.append(f"{label}: expected target cannot appear in confusable_with")
            if candidate_name in clean_confusable:
                errors.append(f"{label}: duplicate confusable target '{candidate_name}'")
            clean_confusable.append(candidate_name)

        if kind == "skill":
            skill_coverage[name] += 1
            route = route_index.get(name)
            if route is None:
                errors.append(f"{label}: expected Skill '{name}' is not registered in skill-routing.json")
            else:
                group_name = route["group"]
                group_coverage[group_name] += 1
                same_group = group_members[group_name]
                if not any(candidate in same_group for candidate in clean_confusable):
                    errors.append(
                        f"{label}: confusable_with must include at least one Skill from "
                        f"routing group '{group_name}'"
                    )
        else:
            workflow_coverage[name] += 1

    for name in sorted(route_index):
        count = skill_coverage[name]
        if count < minimum:
            errors.append(
                f"routed Skill '{name}' has {count} regression case(s); minimum is {minimum}"
            )

    for name in sorted(workflows):
        if workflow_coverage[name] < 1:
            errors.append(f"Workflow '{name}' has no regression case")

    errors.extend(validate_manifest(skills))
    errors.extend(validate_routers(route_index, routing, skills, workflows))

    if errors:
        raise ValidationError("routing regression validation failed:\n- " + "\n- ".join(errors))

    stats = {
        "minimum": minimum,
        "skill_coverage": skill_coverage,
        "workflow_coverage": workflow_coverage,
        "group_coverage": group_coverage,
        "routed_skills": len(route_index),
        "workflows": len(workflows),
    }
    return cases, stats


def normalize_prediction(
    value: Any,
    skills: set[str],
    workflows: set[str],
) -> tuple[str, str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return None
        if ":" in raw:
            prefix, name = raw.split(":", 1)
            prefix = prefix.strip().lower()
            name = name.strip()
            if prefix in {"skill", "workflow"}:
                return prefix, name
        if raw in skills:
            return "skill", raw
        if raw in workflows:
            return "workflow", raw
        return "unknown", raw
    if isinstance(value, dict):
        kind = str(value.get("kind", "")).strip().lower()
        name = str(value.get("name", value.get("prediction", ""))).strip()
        if not kind:
            if name in skills:
                kind = "skill"
            elif name in workflows:
                kind = "workflow"
            else:
                kind = "unknown"
        return kind, name
    return "invalid", str(value)


def load_predictions(path: Path) -> dict[str, Any]:
    raw = load_json(path)
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, list):
        predictions: dict[str, Any] = {}
        for position, item in enumerate(raw, start=1):
            if not isinstance(item, dict):
                raise ValidationError(f"prediction item #{position} must be an object")
            case_id = str(item.get("id", "")).strip()
            if not case_id:
                raise ValidationError(f"prediction item #{position} is missing id")
            if case_id in predictions:
                raise ValidationError(f"duplicate prediction id: {case_id}")
            predictions[case_id] = item.get("prediction", item.get("name"))
        return predictions
    raise ValidationError("predictions file must be a JSON object or array")


def score_predictions(
    cases: list[dict[str, Any]],
    predictions: dict[str, Any],
    skills: set[str],
    workflows: set[str],
) -> bool:
    case_ids = {case["id"] for case in cases}
    unknown_ids = sorted(set(predictions) - case_ids)
    missing_ids = sorted(case_ids - set(predictions))
    failures: list[tuple[str, str, str, str]] = []
    correct = 0
    kind_totals: Counter[str] = Counter()
    kind_correct: Counter[str] = Counter()
    confusion: Counter[tuple[str, str]] = Counter()

    for case in cases:
        case_id = case["id"]
        expected = case["expected"]
        expected_pair = (expected["kind"], expected["name"])
        kind_totals[expected["kind"]] += 1
        predicted = normalize_prediction(predictions.get(case_id), skills, workflows)
        if predicted == expected_pair:
            correct += 1
            kind_correct[expected["kind"]] += 1
            continue
        predicted_label = "<missing>" if predicted is None else f"{predicted[0]}:{predicted[1]}"
        expected_label = f"{expected_pair[0]}:{expected_pair[1]}"
        failures.append((case_id, expected_label, predicted_label, case["input"]))
        confusion[(expected_label, predicted_label)] += 1

    total = len(cases)
    accuracy = correct / total if total else 0.0
    print("\nPrediction score")
    print(f"  Overall:  {correct}/{total} ({accuracy:.1%})")
    for kind in ("skill", "workflow"):
        total_for_kind = kind_totals[kind]
        if total_for_kind:
            print(
                f"  {kind.title():<9}{kind_correct[kind]}/{total_for_kind} "
                f"({kind_correct[kind] / total_for_kind:.1%})"
            )

    if unknown_ids:
        print("\nUnknown prediction IDs:")
        for case_id in unknown_ids:
            print(f"  - {case_id}")
    if missing_ids:
        print(f"\nMissing predictions: {len(missing_ids)}")
    if failures:
        print("\nFailures:")
        for case_id, expected, predicted, user_input in failures:
            print(f"  - {case_id}: expected {expected}, got {predicted}")
            print(f"    input: {user_input}")
        print("\nTop confusions:")
        for (expected, predicted), count in confusion.most_common(10):
            print(f"  - {expected} -> {predicted}: {count}")

    return not unknown_ids and not missing_ids and not failures


def write_template(path: Path, cases: list[dict[str, Any]], force: bool) -> None:
    if path.exists() and not force:
        raise ValidationError(f"refusing to overwrite {path}; pass --force to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    template = {case["id"]: None for case in cases}
    path.write_text(
        json.dumps(template, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Prediction template written: {path}")


def write_evaluation_file(path: Path, cases: list[dict[str, Any]], force: bool) -> None:
    if path.exists() and not force:
        raise ValidationError(f"refusing to overwrite {path}; pass --force to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "instructions": (
            "For each case, choose exactly one AOS Skill or Workflow. "
            "Return a JSON object mapping each case id to the selected name."
        ),
        "cases": [
            {"id": case["id"], "input": case["input"]}
            for case in cases
        ],
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Blind evaluation inputs written: {path}")


def print_static_summary(cases: list[dict[str, Any]], stats: dict[str, Any]) -> None:
    skill_cases = sum(1 for case in cases if case["expected"]["kind"] == "skill")
    workflow_cases = len(cases) - skill_cases
    print("Skill routing regression corpus is valid.")
    print(f"  Cases:          {len(cases)}")
    print(f"  Skill cases:    {skill_cases}")
    print(f"  Workflow cases: {workflow_cases}")
    print(f"  Routed Skills:  {stats['routed_skills']}")
    print(f"  Workflows:      {stats['workflows']}")
    print(f"  Minimum/Skill:  {stats['minimum']}")
    print("  Group coverage:")
    for group, count in stats["group_coverage"].items():
        print(f"    - {group}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate AOS Skill routing regression cases and score Runtime predictions."
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=CASES_FILE,
        help="Regression corpus JSON (default: tests/skill-routing/cases.json)",
    )
    parser.add_argument(
        "--predictions",
        type=Path,
        help="JSON decisions to compare with expected Skill/Workflow routes",
    )
    parser.add_argument(
        "--write-template",
        type=Path,
        help="Write an empty prediction map for all cases",
    )
    parser.add_argument(
        "--write-eval",
        type=Path,
        help="Write blind evaluation inputs without expected routes",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow --write-template to overwrite an existing file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        corpus = load_json(args.cases)
        routing = load_json(ROUTING_FILE)
        skills = collect_named_dirs(SKILLS_DIR, "SKILL.md")
        workflows = collect_named_dirs(WORKFLOWS_DIR, "WORKFLOW.md")
        cases, stats = validate_cases(corpus, routing, skills, workflows)
        print_static_summary(cases, stats)

        if args.write_template:
            write_template(args.write_template, cases, args.force)
        if args.write_eval:
            write_evaluation_file(args.write_eval, cases, args.force)
        if args.predictions:
            predictions = load_predictions(args.predictions)
            if not score_predictions(cases, predictions, skills, workflows):
                return 1
        return 0
    except ValidationError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())