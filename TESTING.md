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

CI runs the self-test, then the validator, then `claude plugin validate` against both
manifests, on every push to `main` and every pull request (`.github/workflows/test.yml`).

The job is named `run-lint`, and that name is load-bearing. GitHub reports the job id as
the status check context, and the "Protect Main Branch" ruleset requires a check called
`run-lint`. Rename the job and the required check never reports, which leaves every pull
request to `main` permanently unmergeable through the normal path.

## What it checks

**Skill definitions** (`*/SKILL.md`, top level only — a wrapper references a
single path segment, so a nested `SKILL.md` could never satisfy the pairing check)
- Frontmatter starts at byte 0, so the loader can actually read it
- Frontmatter is closed by a `---` line of its own — a horizontal rule or a setext
  heading underline in the body cannot masquerade as the closing fence
- Parses as YAML and declares `name`, `description`, `allowed-tools`. `version` is
  deliberately not required: it is not a Claude Code frontmatter field, not one of the
  six Agent Skills spec fields, and carrying it blocks claude.ai packaging.
- `name` matches the directory the skill lives in
- File ends with a newline

**Command wrappers** (`.claude/commands/*.md`)
- Line 1 is the wrapper sentence, which is what the slash-command picker displays.
  A stray comment, a heading, or a leading blank line all fail.
- Line 1 anchors the path with `${CLAUDE_PROJECT_DIR}`. The bare relative form that
  shipped through v1.5.0.1 resolves only when the shell's cwd is the repo root, and
  Claude Code moves that cwd, so it is now rejected outright.
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
  Shape is resolved in a fixed order, and the path counts as much as the content:
  an `interviewee` key marks a switch wherever the file sits, and so does living
  under `switches/` — a patterns or job-map file placed there is still held to the
  switch contract. Then `manifest.yml` by name, then `patterns/` or a `clusters`
  key, then `jobs/` or a `steps` key. A file none of those place is parsed but not
  shape-checked.
- Parse errors report type and position only, never the offending source line.
  These files hold interviewee names and verbatim quotes, and CI logs outlive the
  file they came from.

**Plugin manifest** (`.claude-plugin/plugin.json`)

This is the only path an installed user has to these skills, and every way it breaks
is silent — the command simply does not exist, with no error anywhere. So each way is
its own check:
- The manifest exists at all
- It is valid JSON
- `skills` is a list
- Every entry is a relative path starting `./`
- Every entry resolves to a directory containing a `SKILL.md`
- Every skill directory on disk appears in the list. A skill the manifest omits ships
  to nobody, which is the same outcome as not shipping it.

CI additionally runs `claude plugin validate` against `.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json`. That is the authoritative check, maintained against
the real plugin loader; the checks above mirror the path resolution so contributors
without the Claude Code CLI still catch the common mistake locally. The marketplace
manifest is validated with `--strict`; the plugin manifest is not, because `--strict`
reports this repo's own `CLAUDE.md` at the plugin root as a warning, and that is a
repo layout fact rather than a defect.

**Skill runtime contracts** (`*/SKILL.md`)
- A skill containing a ```bash block declares `Bash` in `allowed-tools`. Without it the
  block never runs and nothing says so: `/jtbd-demo` shipped that way from v1.0.0 to
  v1.6.0.1, its skills-root resolution dead code the whole time.
- A skill that assigns `_JTBD_SKILLS` probes `${CLAUDE_PLUGIN_ROOT}`. A resolver that
  checks only the repo root and `~/.claude/skills/jtbd` finds nothing under a plugin
  install, which is where every installed user actually is. That is the v1.6.0.0
  regression, and this is what stops it recurring.

**Availability claims** (every `.md`)
- Every shipped skill is listed in both `README.md` and `CLAUDE.md`. That rule has
  no escapes: the three below belong to the "coming soon" check alone.
- No skill that ships in this repo is advertised as "coming soon", in prose or in a
  README table cell.

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
skill, a dangling `SKILL.md`
reference, a `Coming soon` table cell, a neighbouring clause trying to defuse one,
unparseable YAML, an incomplete switch analysis, a switch analysis missing
`interviewee`, an unadvertised skill, and six ways the plugin manifest can silently
drop a command: absent, malformed JSON, no `skills` list, an entry that is not
`./`-relative, an entry that resolves to no `SKILL.md`, and a skill on disk the list
omits. Two more pin the runtime contracts: a bash block in a skill that does not declare
`Bash`, and a `_JTBD_SKILLS` resolver that never probes `${CLAUDE_PLUGIN_ROOT}` (with a
positive case proving a resolver that does probe is accepted). Disabling any of those
check bodies fails the self-test.

Separately, and not via a fixture, `self_test()` asserts the `WRAPPER_LINE1` regex
directly against the wrapper line 1 forms it must reject: blank, a comment, a heading,
a parent traversal, and the pre-v1.6.0.0 bare relative path. Whole runs take about 0.7s.

`self_test()` reports failures explicitly instead of using `assert`, because
`python3 -O` strips assertions. Keep it that way: a self-test that passes under
`-O` while testing nothing is the exact bug this file exists to catch, and this
suite shipped with it once.
