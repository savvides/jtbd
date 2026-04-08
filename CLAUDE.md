# jtbd

Open source Claude Code skills for the Jobs to Be Done framework. Helps startup founders turn customer interview transcripts into structured, version-controlled demand evidence.

## Skills

- `/jtbd-demo` — 5-minute guided walkthrough of JTBD for new users
- `/jtbd-switch` — Analyze one interview transcript into a structured Switch analysis (YAML)
- `/jtbd-interview` — Generate a customized Switch interview script

## Architecture

- Skills are SKILL.md files in their own directories (`jtbd-switch/`, `jtbd-interview/`, etc.)
- User data lives in `.jtbd/` in the user's repo (not this repo)
- No external dependencies. No build step. No compiled binaries.
- Optional gstack integration detected at runtime via path check

## YAML Schema

Switch analysis files use `schema_version: 1`. See `examples/expected-output.yml` for the full schema. See `demo/.jtbd/` for a populated example project.

## Skill routing

When the user's request matches an available skill, invoke it using the Skill tool.

Key routing rules:
- Demo, tutorial, how does this work, show me, getting started → invoke jtbd-demo
- Analyze interview, customer interview, switching analysis → invoke jtbd-switch
- Interview script, interview guide, how to interview → invoke jtbd-interview
