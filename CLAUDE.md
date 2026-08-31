# jtbd

Open source Claude Code skills for the Jobs to Be Done framework. Helps startup founders turn customer interview transcripts into structured, version-controlled demand evidence.

## Skills

- `/jtbd-demo` — 5-minute guided walkthrough of JTBD for new users
- `/jtbd-switch` — Analyze one interview transcript into a structured Switch analysis (YAML)
- `/jtbd-interview` — Generate a customized Switch interview script
- `/jtbd-patterns` — Find cross-interview patterns across 3+ switch analyses
- `/jtbd-pipeline` — Batch-process multiple transcripts through the full analysis pipeline
- `/jtbd-forces` (Preview) — Generates an HTML diagram of the four forces
- `/jtbd-map` (Preview) — Synthesizes patterns into a structured Job Map (YAML + Markdown)
- `/jtbd-brief` (Preview) — Drafts a JTBD-native product brief from Job Map data

The three Preview skills run, but `/jtbd-map` emits a schema that does not carry every
field `/jtbd-brief` requires, so on the default path part of a generated brief has no
source in the user's data. README states this for users; TODOS.md tracks the fix.

## Architecture

- Skills are SKILL.md files in their own directories (`jtbd-switch/`, `jtbd-interview/`, etc.)
- The repo is itself a Claude Code plugin. `.claude-plugin/marketplace.json` and
  `.claude-plugin/plugin.json` sit at the root, and `plugin.json`'s `skills` array lists
  every skill directory. That array is how installed users reach these skills: a path that
  does not resolve drops one command with no error.
- `.claude/commands/*.md` wrappers exist only for working inside this repo. They must be
  anchored with `${CLAUDE_PROJECT_DIR}` — a bare relative path resolves only when the
  shell's cwd happens to be the repo root, and Claude Code moves that cwd.
- User data lives in `.jtbd/` in the user's repo (not this repo)
- The skills need no external dependencies, no build step, no compiled binaries. `scripts/validate.py` needs PyYAML.
- Optional gstack integration detected at runtime via path check

## YAML Schema

Switch analysis files carry `interviewee`, `timeline`, `forces`, `job_story` and `evidence_strength`.
See `examples/expected-output.yml` for the full schema. `manifest.yml` and patterns files carry `schema_version: 1`. See `demo/.jtbd/` for a populated example project.

## Skill routing

When the user's request matches an available skill, invoke it using the Skill tool.

Key routing rules:
- Demo, tutorial, how does this work, show me, getting started → invoke jtbd-demo
- Analyze interview, customer interview, switching analysis → invoke jtbd-switch
- Interview script, interview guide, how to interview → invoke jtbd-interview
- Find patterns, cross-interview, what are the jobs → invoke jtbd-patterns
- Batch analysis, process all interviews, pipeline, analyze all transcripts → invoke jtbd-pipeline
- Draw forces, forces diagram, forces visualization → invoke jtbd-forces
- Create job map, job mapping, friction, opportunities → invoke jtbd-map
- Product brief, prd, brief, pitch → invoke jtbd-brief

## Testing

Run: `python3 scripts/validate.py` (validates skill frontmatter, command wrappers,
the plugin manifest, YAML example data, and availability claims). CI runs `--self-test`,
then the validator, then `claude plugin validate` against both manifests, on every push
to `main` and every pull request. See TESTING.md for what each check covers and why.

Expectations:
- When you add a skill, add `.claude/commands/<name>.md` AND a `./<name>` entry in
  `.claude-plugin/plugin.json` in the same change. The wrapper must reference the skill its
  filename names — the validator checks pairing, not just presence — and a skill missing
  from the manifest is invisible to every installed user.
- Skill frontmatter carries `name`, `description` and `allowed-tools`. Do not add `version`:
  it is not a Claude Code field, not one of the six Agent Skills spec fields, and it blocks
  claude.ai packaging. The plugin manifest holds the collection's version.
- A skill with a ```bash block must list `Bash` in `allowed-tools`. `/jtbd-demo` did not,
  from v1.0.0 to v1.6.0.1, so its whole preamble silently never ran.
- A skill that resolves the skills root to reach a bundled file (`examples/`, `demo/`,
  another skill's `SKILL.md`) must probe `${CLAUDE_PLUGIN_ROOT}` first, then the repo,
  then a legacy clone last — and must anchor every path it reads *and every path it tells
  the user to type* to that root. Plugin installs live under `~/.claude/plugins/`, and a
  bare relative path resolves to the user's own project, where nothing is.
- When you add a new file type under `.jtbd/`, add an example to `demo/.jtbd/` and make sure it parses.
- When you add a check to `scripts/validate.py`, prove it fails on the bug it targets before committing.
- Never commit a change that makes the validator fail.
