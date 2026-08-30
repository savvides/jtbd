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

```bash
python3 scripts/validate.py --self-test
```

Runs the fixture suite instead of the repo, and returns before reading a single
repo file. Run it whenever you touch `scripts/validate.py`: a plain
`validate.py` run never exercises a fixture, so a broken one passes locally and
fails in CI.

PyYAML is required and the script exits with an install hint without it. That is
deliberate: an earlier version degraded to a partial no-op when PyYAML was absent
and still printed "All checks passed", which is the one failure mode a validator
must never have.

CI runs the self-test and then the validator on every push to `main` and every
pull request (`.github/workflows/test.yml`).

## What it checks

**Skill definitions** (`*/SKILL.md`, top level only — a wrapper references a
single path segment, so a nested `SKILL.md` could never satisfy the pairing check)
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

**Example and demo data** (every `.yml` / `.yaml` outside `.github/`)
- Parses. The `.jtbd/` directory is version-controlled evidence, and the machine
  readable half is worthless if it does not load.
- Each document carries the keys its shape documents: switch analyses
  (`interviewee`, `timeline`, `forces`, `job_story`, `evidence_strength`), patterns
  files (`schema_version`, `clusters`, `force_patterns`), job maps (`job`, `steps`),
  and `manifest.yml` (`schema_version`, `product`, `target_user`, `settings`).
  Shape is read from the document's own content where it can be, so a non-switch
  file living under `switches/` is not forced into the wrong contract.
- Parse errors report type and position only, never the offending source line.
  These files hold interviewee names and verbatim quotes, and CI logs outlive the
  file they came from.

**Availability claims** (every `.md`)
- No skill that ships in this repo is advertised as "coming soon", in prose or in a
  README table cell.
- Every shipped skill is listed in both `README.md` and `CLAUDE.md`.

  Three escapes exist, because truthful prose can name a skill and "coming soon" on
  one line. `CHANGELOG.md` and `docs/superpowers/` are exempt outright — they are
  historical records. Elsewhere, a line reading as past tense ("no longer", "was
  marked", "previously") is allowed, and `<!-- validate: allow-coming-soon -->` on
  the line is an explicit opt-out.

The file list comes from `git ls-files` plus untracked-but-not-ignored files, so a
skill you have created and not yet staged is still validated.

## Adding a check

Add a `check_*(files, skill_dirs)` function returning the set of repo-relative
paths it inspected, add it to `CHECKS`, and report problems with `fail(path, message)`.

Then add a case to `self_test()`. It builds throwaway git repos with
`_run_fixture()` and asserts your check fires, so CI proves behaviour rather than
pattern-matching. A manual proof only covers the day you wrote it.

Fixtures currently pin: displaced frontmatter, a name/directory mismatch, a missing
trailing newline, a skill with no wrapper, a wrapper whose line 1 runs a different
skill, a dangling `SKILL.md` reference, a `Coming soon` table cell, a neighbouring
clause trying to defuse one, unparseable YAML, an incomplete switch analysis, a
switch analysis missing `interviewee`, and an unadvertised skill. Disabling any of
those check bodies fails the self-test. Whole runs take about 0.4s.

`self_test()` reports failures explicitly instead of using `assert`, because
`python3 -O` strips assertions. Keep it that way: a self-test that passes under
`-O` while testing nothing is the exact bug this file exists to catch, and this
suite shipped with it once.
