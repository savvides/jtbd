# Testing

This repo ships Markdown skill definitions and YAML example data, not application
code, so it has no unit tests. What it has instead is a structural contract, and
that contract breaks silently. A `SKILL.md` whose YAML frontmatter does not start
at byte 0 loses its `name`, `description` and `allowed-tools` — and the diff looks
completely normal. That exact bug shipped in v1.4.0.0.

`scripts/validate.py` enforces the contract.

## How to run

```bash
python3 scripts/validate.py
```

Exits 0 when everything passes, 1 with a list of failures otherwise.

PyYAML is required and the script exits with an install hint without it. That is
deliberate: an earlier version degraded to a partial no-op when PyYAML was absent
and still printed "All checks passed", which is the one failure mode a validator
must never have.

CI runs the self-test and then the validator on every push to `main` and every
pull request (`.github/workflows/test.yml`).

## What it checks

**Skill definitions** (`**/SKILL.md`)
- Frontmatter starts at byte 0, so the loader can actually read it
- Frontmatter is closed by a `---` line of its own — a horizontal rule or a setext
  heading underline in the body cannot masquerade as the closing fence
- Parses as YAML and declares `name`, `version`, `description`, `allowed-tools`
- `name` matches the directory the skill lives in
- File ends with a newline

**Command wrappers** (`.claude/commands/*.md`)
- Line 1 is the wrapper sentence, which is what the slash-command picker displays.
  A stray comment, a heading, or a leading blank line all fail.
- Each wrapper references a `SKILL.md` that exists on disk
- Each wrapper is *paired* with the skill its filename names. Coverage is not
  pairing: two wrappers with swapped targets would each run the wrong skill.
- Every skill directory has its own wrapper
- File ends with a newline

**Example and demo data** (every `.yml` / `.yaml`)
- Parses. The `.jtbd/` directory is version-controlled evidence, and the machine
  readable half is worthless if it does not load.
- Switch analyses carry their documented top-level keys (`interviewee`, `timeline`,
  `forces`, `job_story`, `evidence_strength`), matching `examples/expected-output.yml`.
- Parse errors report type and position only, never the offending source line.
  These files hold interviewee names and verbatim quotes, and CI logs outlive the
  file they came from.

**Availability claims** (every `.md`)
- No skill that ships in this repo is advertised as "coming soon", in prose or in a
  README table cell. Dated plans and specs under `docs/superpowers/` are exempt —
  they are a historical record.
- Every shipped skill is listed in both `README.md` and `CLAUDE.md`.

The file list comes from `git ls-files` plus untracked-but-not-ignored files, so a
skill you have created and not yet staged is still validated.

## Adding a check

Add a `check_*(files, skill_dirs)` function returning the number of files it
inspected, add it to `CHECKS`, and report problems with `fail(path, message)`.

Then prove it works: break the thing it checks, confirm the script fails, and
restore. A check that never fails is not a check. If the check has a pure helper
(a regex, a parser), add an assertion to `self_test()` so CI proves it still
rejects what it was written to reject — the manual proof only covers the day you
wrote it.
