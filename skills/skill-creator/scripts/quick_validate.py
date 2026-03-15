#!/usr/bin/env python3
"""
Quick validation for repository skills.

This script stays dependency-light so contributors can run it in a clean Python
environment without installing PyYAML first.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KNOWN_KEYS = {
    "name",
    "description",
    "category",
    "risk",
    "source",
    "date_added",
    "author",
    "tags",
    "tools",
    "version",
    "license",
    "allowed-tools",
    "metadata",
}


def extract_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith("---"):
        raise ValueError("No YAML frontmatter found.")

    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError("Invalid frontmatter format.")

    raw_frontmatter = match.group(1)
    body = match.group(2)
    return parse_frontmatter(raw_frontmatter), body


def parse_frontmatter(raw_frontmatter: str) -> dict:
    if yaml is not None:
        parsed = yaml.safe_load(raw_frontmatter)
        if not isinstance(parsed, dict):
            raise ValueError("Frontmatter must decode to a mapping.")
        return parsed

    parsed: dict[str, object] = {}
    for raw_line in raw_frontmatter.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(
                "PyYAML is not installed and a frontmatter line could not be parsed: "
                f"{raw_line!r}"
            )

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if not value:
            parsed[key] = ""
            continue

        if value[0] == value[-1] and value[0] in {"'", '"'}:
            parsed[key] = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            try:
                parsed[key] = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                items = [item.strip().strip("'\"") for item in value[1:-1].split(",")]
                parsed[key] = [item for item in items if item]
        else:
            parsed[key] = value

    return parsed


def validate_skill(skill_path: str | Path) -> tuple[bool, str]:
    errors: list[str] = []
    warnings: list[str] = []

    skill_dir = Path(skill_path)
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return False, "SKILL.md not found."

    try:
        content = skill_md.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"Unable to read SKILL.md: {exc}"

    try:
        frontmatter, body = extract_frontmatter(content)
    except ValueError as exc:
        return False, str(exc)

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not isinstance(name, str) or not name.strip():
        errors.append("Missing or invalid 'name' in frontmatter.")
    else:
        normalized_name = name.strip()
        if not SKILL_NAME_PATTERN.fullmatch(normalized_name):
            errors.append(
                "Name must use lowercase letters, digits, and single hyphens only."
            )
        if normalized_name != skill_dir.name:
            errors.append(
                f"Frontmatter name '{normalized_name}' does not match directory '{skill_dir.name}'."
            )
        if len(normalized_name) > 64:
            errors.append("Name must be 64 characters or fewer.")

    if not isinstance(description, str) or not description.strip():
        errors.append("Missing or invalid 'description' in frontmatter.")
    else:
        normalized_description = description.strip()
        if "<" in normalized_description or ">" in normalized_description:
            errors.append("Description cannot contain angle brackets.")
        if len(normalized_description) > 1024:
            errors.append("Description must be 1024 characters or fewer.")

    if not body.strip():
        errors.append("SKILL.md body is empty.")

    unknown_keys = sorted(set(frontmatter.keys()) - KNOWN_KEYS)
    if unknown_keys:
        warnings.append("Unknown frontmatter keys: " + ", ".join(unknown_keys))

    messages = errors + warnings
    if messages:
        return (not errors), " ".join(messages)

    return True, "Skill is valid."


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        return 1

    is_valid, message = validate_skill(sys.argv[1])
    print(message)
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
