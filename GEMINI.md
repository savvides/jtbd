# jtbd

Open source skills for the Jobs to Be Done framework, supporting Google Antigravity, Gemini, and Claude Code. Helps startup founders turn customer interview transcripts into structured, version-controlled demand evidence.

## Skills

- `/jtbd-demo` — 5-minute guided walkthrough of JTBD for new users
- `/jtbd-switch` — Analyze one interview transcript into a structured Switch analysis (YAML)
- `/jtbd-interview` — Generate a customized Switch interview script
- `/jtbd-patterns` — Find cross-interview patterns across 3+ switch analyses
- `/jtbd-pipeline` — Batch-process multiple transcripts through the full analysis pipeline
- `/jtbd-forces` — Generate an HTML diagram of the four forces
- `/jtbd-map` — Synthesize patterns into a structured Job Map (YAML + Markdown)
- `/jtbd-brief` — Draft a JTBD-native product brief from Job Map data

## Architecture

- Skills are standard Agent Skills `SKILL.md` files in their own directories (`jtbd-switch/`, `jtbd-interview/`, etc.)
- Cross-platform agent compatibility:
  - Antigravity / Gemini: Discovered via workspace root, `GEMINI.md`/`AGENTS.md`, and `plugins/jtbd/plugin.json` or `~/.gemini/config/plugins/jtbd`.
  - Claude Code: Managed via `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` at root, plus `.claude/commands/*.md` wrappers for in-repo work.
- User data lives in `.jtbd/` in the user's repo (not this repo)
- The skills need no external dependencies, no build step, no compiled binaries. `scripts/validate.py` needs PyYAML.
- Optional gstack integration detected at runtime via path check

## YAML Schema

Switch analysis files carry `interviewee`, `timeline`, `forces`, `job_story` and `evidence_strength`.
See `examples/expected-output.yml` for the full schema. `manifest.yml` and patterns files carry `schema_version: 1`. See `demo/.jtbd/` for a populated example project.

## Skill routing

When the user's request matches an available skill, invoke it using the appropriate skill invocation tool or command.

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
the plugin manifests, YAML example data, and availability claims). CI runs `--self-test`,
then the validator, then `claude plugin validate` against both manifests, on every push
to `main` and every pull request. See TESTING.md for what each check covers and why.

Expectations:
- When you add a skill, add `.claude/commands/<name>.md` AND an entry in both
  `.claude-plugin/plugin.json` and `plugins/jtbd/plugin.json` in the same change.
- List all shipped skills in `README.md`, `CLAUDE.md`, and `GEMINI.md`.
- Skill frontmatter carries `name`, `description` and `allowed-tools`. Do not add `version`:
  it is not a standard frontmatter field and blocks claude.ai packaging.
- A skill with a ```bash block must list `Bash` in `allowed-tools`.
- A skill that resolves the skills root to reach bundled files (`examples/`, `demo/`,
  another skill's `SKILL.md`) must probe `${CLAUDE_PLUGIN_ROOT}` and Antigravity plugin paths,
  falling back to the repo root and legacy clones last.
- When you add a new file type under `.jtbd/`, add an example to `demo/.jtbd/` and make sure it parses.
- When you add a check to `scripts/validate.py`, prove it fails on the bug it targets before committing.
- Never commit a change that makes the validator fail.
