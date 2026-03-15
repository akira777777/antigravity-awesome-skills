---
name: skill-creator
description: "Create or update skills in this repository using the local scaffold and validator. Use when adding a new skill, fixing SKILL.md frontmatter, reorganizing bundled resources, or improving skill authoring docs."
category: meta
risk: safe
source: community
date_added: "2026-02-27"
---

# Skill Creator

## Overview

Use this skill to create or modernize repository skills without drifting from the
project's conventions. Prefer the local scaffold and validator over ad-hoc file
creation so new skills stay consistent with the contributor docs and the actual
layout used in `skills/`.

## Source of Truth

Read these files in order:

1. `../../docs/contributors/skill-template.md`
2. `../../docs/contributors/skill-anatomy.md`
3. `../../CONTRIBUTING.md`
4. `scripts/init_skill.py`
5. `scripts/quick_validate.py`

Load `references/workflows.md` only if the skill being authored needs explicit
workflow branching patterns.

## Workflow

1. Clarify the skill outcome.
   Gather the user request, 2-4 trigger examples, and whether this is a new skill
   or an update to an existing one.

2. Inspect nearby skills before writing.
   Find the closest existing skills in `skills/` and reuse their structure where
   it fits. Avoid creating near-duplicates.

3. Decide the minimum resource set.
   Create only the directories that add real value:
   - `scripts/` for deterministic helpers
   - `references/` for on-demand docs
   - `assets/` for reusable output files
   - `examples/` for fixtures or sample inputs
   - `templates/` for starter files

4. Initialize new skills with the scaffold.

   ```bash
   python scripts/init_skill.py <skill-name> --path <skills-dir> [--resources scripts,references] [--examples]
   ```

   Use lowercase hyphen-case names only. The folder name must match the
   `name` frontmatter exactly.

5. Edit the skill for repository conventions.
   - Keep frontmatter compatible with `docs/contributors/skill-template.md`
   - Make the `description` precise enough to trigger the skill reliably
   - Keep `SKILL.md` focused on workflow and decision-making
   - Move long reference material out of `SKILL.md` when it starts becoming bulky
   - Do not create extra documentation files by default; add them only when the
     repository clearly benefits from them

6. Validate before finishing.

   ```bash
   python scripts/quick_validate.py <path-to-skill>
   ```

   Treat validation errors as blockers. Fix warnings when they signal drift or
   ambiguity.

7. Smoke-test the authoring flow when the scaffold changed.
   Create a temporary skill, validate it, and delete it once the check passes.

## Updating Existing Skills

- Preserve the existing skill name unless there is a strong reason to rename it.
- Check whether generated docs or indexes rely on current frontmatter keys before
  removing metadata.
- When refactoring structure, update any referenced resource paths in `SKILL.md`
  in the same change.

## Writing Guidance

- Prefer imperative instructions over generic advice.
- Use concrete trigger phrases in the `description`.
- Keep examples realistic and short.
- Default to concise `SKILL.md`; use bundled resources for everything long or
  highly specific.

## Validation Checklist

- `SKILL.md` exists and frontmatter parses cleanly.
- `name` matches the folder name.
- `description` is present and specific.
- Referenced directories and files actually exist.
- Placeholder files are removed or replaced if they are no longer useful.

## Related Files

- `README.md` in this folder for a quick operator-facing summary
- `references/workflows.md` for branching workflow examples
- `references/output-patterns.md` if you need sample output conventions
