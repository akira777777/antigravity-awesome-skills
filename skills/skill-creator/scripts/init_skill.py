#!/usr/bin/env python3
"""
Skill Initializer - create a new skill skeleton that matches this repository.

Usage:
    init_skill.py <skill-name> --path <output-directory>
        [--resources scripts,references,assets,examples,templates]
        [--examples]
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


DEFAULT_CATEGORY = "general"
DEFAULT_RISK = "safe"
DEFAULT_SOURCE = "community"
VALID_RESOURCES = {"scripts", "references", "assets", "examples", "templates"}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

SKILL_TEMPLATE = """---
name: {skill_name}
description: "TODO: Explain what this skill does and when it should trigger."
category: {category}
risk: {risk}
source: {source}
date_added: "{date_added}"
---

# {skill_title}

## Overview

TODO: Summarize the capability in 2-4 sentences. Focus on what the skill enables
and what is non-obvious about using it well.

## When to Use This Skill

- Use when TODO: describe the user request or situation that should trigger this skill.
- Use when TODO: mention concrete technologies, file types, or workflows.
- Use when TODO: explain the highest-value scenario for this skill.

## Workflow

1. Gather the minimum context required to execute safely.
2. Choose the narrowest set of bundled resources that actually helps.
3. Execute the task.
4. Validate the result before reporting completion.

## Resources

TODO: Delete lines for directories you did not create.
- `scripts/`: deterministic helpers or automation.
- `references/`: documentation worth loading on demand.
- `assets/`: files meant to be copied or reused in output.
- `examples/`: fixtures or sample inputs.
- `templates/`: starter files.

## Notes

- Keep frontmatter aligned with [`docs/contributors/skill-template.md`](../../docs/contributors/skill-template.md).
- Keep content concise and move long material to `references/` when possible.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Minimal helper script for {skill_name}.
Replace with real logic or delete this file if the skill does not need scripts.
"""


def main() -> None:
    print("Replace this placeholder with real automation.")


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} Reference

Use this file for detailed material that would bloat `SKILL.md`.

Suggested sections:
- Context or background
- Constraints and edge cases
- Examples worth loading on demand
"""

EXAMPLE_ASSET = """This placeholder represents a reusable asset.

Replace it with a real template, fixture, image, or boilerplate file, or delete it.
"""

EXAMPLE_MARKDOWN = """# Example

Describe one realistic way to use this skill.
"""

EXAMPLE_TEMPLATE = """// Replace with a real starter template used by this skill.
"""


def title_case_skill_name(skill_name: str) -> str:
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def validate_skill_name(skill_name: str) -> None:
    if len(skill_name) > 64:
        raise ValueError("Skill name must be 64 characters or fewer.")
    if not SKILL_NAME_PATTERN.fullmatch(skill_name):
        raise ValueError(
            "Skill name must use lowercase letters, digits, and single hyphens only."
        )


def parse_resources(raw_resources: str | None) -> list[str]:
    if not raw_resources:
        return []

    resources = []
    for item in raw_resources.split(","):
        resource = item.strip().lower()
        if not resource:
            continue
        if resource not in VALID_RESOURCES:
            valid = ", ".join(sorted(VALID_RESOURCES))
            raise ValueError(f"Unknown resource '{resource}'. Valid values: {valid}")
        resources.append(resource)
    return resources


def write_text(path: Path, content: str, executable: bool = False) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")
    if executable:
        path.chmod(0o755)


def create_examples(skill_dir: Path, skill_name: str, skill_title: str, resources: list[str]) -> None:
    for resource in resources:
        if resource == "scripts":
            write_text(
                skill_dir / "scripts" / "example.py",
                EXAMPLE_SCRIPT.format(skill_name=skill_name),
                executable=True,
            )
        elif resource == "references":
            write_text(
                skill_dir / "references" / "reference.md",
                EXAMPLE_REFERENCE.format(skill_title=skill_title),
            )
        elif resource == "assets":
            write_text(skill_dir / "assets" / "README.txt", EXAMPLE_ASSET)
        elif resource == "examples":
            write_text(skill_dir / "examples" / "example.md", EXAMPLE_MARKDOWN)
        elif resource == "templates":
            write_text(skill_dir / "templates" / "template.txt", EXAMPLE_TEMPLATE)


def init_skill(skill_name: str, output_dir: str, resources: list[str], add_examples: bool) -> Path:
    validate_skill_name(skill_name)

    skill_dir = Path(output_dir).resolve() / skill_name
    if skill_dir.exists():
        raise FileExistsError(f"Skill directory already exists: {skill_dir}")

    skill_dir.mkdir(parents=True, exist_ok=False)

    skill_title = title_case_skill_name(skill_name)
    skill_md = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title,
        category=DEFAULT_CATEGORY,
        risk=DEFAULT_RISK,
        source=DEFAULT_SOURCE,
        date_added=date.today().isoformat(),
    )
    write_text(skill_dir / "SKILL.md", skill_md)

    for resource in resources:
        (skill_dir / resource).mkdir(exist_ok=True)

    if add_examples:
        create_examples(skill_dir, skill_name, skill_title, resources)

    return skill_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a new skill skeleton for this repository."
    )
    parser.add_argument("skill_name", help="Hyphen-case skill identifier.")
    parser.add_argument(
        "--path",
        required=True,
        dest="output_dir",
        help="Directory where the skill folder should be created.",
    )
    parser.add_argument(
        "--resources",
        help="Comma-separated list of resource directories to create.",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Populate created resource directories with placeholder examples.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        resources = parse_resources(args.resources)
        skill_dir = init_skill(
            args.skill_name,
            args.output_dir,
            resources,
            args.examples,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"Created skill at: {skill_dir}")
    print("Next steps:")
    print("1. Update SKILL.md with a precise trigger description and workflow.")
    if resources:
        print("2. Replace or delete placeholder files in the resource directories.")
        print("3. Validate the skill with scripts/quick_validate.py before committing.")
    else:
        print("2. Add only the resource directories you truly need.")
        print("3. Validate the skill with scripts/quick_validate.py before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
