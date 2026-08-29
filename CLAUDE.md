# jtbd

Open source Claude Code skills for the Jobs to Be Done framework. Helps startup founders turn customer interview transcripts into structured, version-controlled demand evidence.

## Skills

- `/jtbd-demo` — 5-minute guided walkthrough of JTBD for new users
- `/jtbd-switch` — Analyze one interview transcript into a structured Switch analysis (YAML)
- `/jtbd-interview` — Generate a customized Switch interview script
- `/jtbd-patterns` — Find cross-interview patterns across 3+ switch analyses
- `/jtbd-pipeline` — Batch-process multiple transcripts through the full analysis pipeline
- `/jtbd-forces` — Generates an HTML diagram of the four forces
- `/jtbd-map` — Synthesizes patterns into a structured Job Map (YAML + Markdown)
- `/jtbd-brief` — Drafts a JTBD-native product brief from Job Map data

## Architecture

- Skills are SKILL.md files in their own directories (`jtbd-switch/`, `jtbd-interview/`, etc.)
- User data lives in `.jtbd/` in the user's repo (not this repo)
- No external dependencies. No build step. No compiled binaries.
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
YAML example data, and availability claims). CI runs `--self-test` and then the
validator, on every push to `main` and every pull request. See TESTING.md for what
each check covers and why.

Expectations:
- When you add a skill, add `.claude/commands/<name>.md` in the same change. The wrapper must reference the skill its filename names — the validator checks pairing, not just presence.
- When you add a new file type under `.jtbd/`, add an example to `demo/.jtbd/` and make sure it parses.
- When you add a check to `scripts/validate.py`, prove it fails on the bug it targets before committing.
- Never commit a change that makes the validator fail.
