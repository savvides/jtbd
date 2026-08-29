# Testing

100% test coverage is the key to great vibe coding. Tests let you move fast, trust
your instincts, and ship with confidence. Without them, vibe coding is just yolo
coding. With them, it's a superpower.

This repo ships Markdown skill definitions and YAML example data, not application
code, so it has no unit tests. What it has instead is a structural contract, and
that contract breaks silently. A `SKILL.md` whose YAML frontmatter does not start
at byte 0 loses its `name`, `description` and `allowed-tools` — and the diff looks
completely normal. That exact bug shipped in v1.4.0.0.

## How to run

```bash
python3 scripts/validate.py
```

Exits 0 when everything passes, 1 with a list of failures otherwise. The only
dependency is PyYAML, which the skills themselves already rely on for their
`Validate Output` steps. Without it the script still runs and skips the YAML
parse checks.

CI runs the same command on every push and pull request
(`.github/workflows/test.yml`).

## What it checks

**Skill definitions** (`*/SKILL.md`)
- Frontmatter starts at byte 0, so the loader can actually read it
- Frontmatter parses as YAML and declares `name`, `version`, `description`, `allowed-tools`
- `name` matches the directory the skill lives in
- File ends with a newline

**Command wrappers** (`.claude/commands/*.md`)
- Reference a `SKILL.md` that exists on disk
- Carry no stray comment on line 1, which otherwise displaces the description in
  the slash-command picker
- Every skill directory has a wrapper
- File ends with a newline

**Example and demo data** (every tracked `.yml` / `.yaml`)
- Parses. The `.jtbd/` directory is version-controlled evidence, and the machine
  readable half is worthless if it does not load.

**Availability claims** (every tracked `.md`)
- No skill that ships in this repo is advertised as `(coming soon)`. Dated plans
  and specs under `docs/superpowers/` are exempt — they are a historical record.

## Adding a check

Add a `check_*` function in `scripts/validate.py`, call it from `main()`, and
report problems with `fail(path, message)`. Then prove it works: break the thing
it checks, confirm the script fails, and restore. A check that never fails is
not a check.
