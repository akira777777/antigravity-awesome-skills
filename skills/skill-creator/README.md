# skill-creator

Repository-local tooling and guidance for authoring skills in
`antigravity-awesome-skills`.

## What it does

This folder gives maintainers a practical workflow for creating or updating
skills without guessing the expected shape:

- `SKILL.md` explains the authoring flow
- `scripts/init_skill.py` scaffolds a new skill folder
- `scripts/quick_validate.py` validates frontmatter and basic structure
- `references/` contains supplemental patterns when the main file should stay lean

## Recommended workflow

1. Review repository conventions:
   - [`../../docs/contributors/skill-template.md`](../../docs/contributors/skill-template.md)
   - [`../../docs/contributors/skill-anatomy.md`](../../docs/contributors/skill-anatomy.md)
   - [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md)
2. Create a scaffold:

   ```bash
   python scripts/init_skill.py my-skill --path ../../skills --resources scripts,references --examples
   ```

3. Edit the generated `SKILL.md` and remove any placeholder files you do not need.
4. Validate the result:

   ```bash
   python scripts/quick_validate.py ../../skills/my-skill
   ```

## Scaffold flags

- `--path`: required target directory for the new skill folder
- `--resources`: optional comma-separated directories to create
- `--examples`: populate created resource directories with placeholder files

Supported resource directories:

- `scripts`
- `references`
- `assets`
- `examples`
- `templates`

## Notes

- The scaffold follows this repository's extended frontmatter conventions, not a
  stripped-down external format.
- `quick_validate.py` works without `PyYAML`; it falls back to a small parser when
  the dependency is unavailable.
- Do not keep placeholder files you are not actively using.
