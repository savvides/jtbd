# Contributing to jtbd

Thanks for wanting to contribute. Here's how.

## Adding a new skill

Each skill is a directory with a single `SKILL.md` file:

```
jtbd-yourskill/
└── SKILL.md

.claude/commands/
└── jtbd-yourskill.md

.claude-plugin/plugin.json      <- add "./jtbd-yourskill" to the "skills" array
plugins/jtbd/skills/             <- add symlink or entry for Antigravity plugin
```

The `SKILL.md` needs:

1. **YAML frontmatter** with `name`, `description`, and `allowed-tools`. Do not add
   `version` — it is not a standard frontmatter field, and the plugin manifest is
   the single source of truth for the collection's version.
2. **A preamble bash block** that detects `.jtbd/` and gstack. If you include one, list
   `Bash` in `allowed-tools` or it never runs. If your skill reads anything bundled with
   the plugin, resolve the root by probing `${CLAUDE_PLUGIN_ROOT}` and Antigravity paths
   (see `jtbd-demo/SKILL.md`), and anchor every bundled path to it — including paths you print
   for the user to type. The validator enforces both.
3. **Clear instructions** for the agent on what to extract/generate
4. **An example output** showing the exact expected format
5. **A human review step** using AskUserQuestion before writing files

You also need three more things, and CI fails without them:

- `.claude/commands/<your-skill>.md`, a one-line wrapper pointing at your `SKILL.md`,
  anchored with `${CLAUDE_PROJECT_DIR}`. This makes the command work inside Claude Code.
- An entry in the `skills` array of `.claude-plugin/plugin.json` and in `plugins/jtbd/skills/`.
- Listings in `README.md`, `CLAUDE.md`, and `GEMINI.md`.

Before opening a PR, run `python3 scripts/validate.py`. See TESTING.md for what it
checks.

Look at `jtbd-switch/SKILL.md` or `jtbd-interview/SKILL.md` as reference implementations.

## YAML schema

`manifest.yml` and patterns files use `schema_version: 1`; switch analyses and job maps do not. If you're adding a skill that writes new file types to `.jtbd/`, document the schema in your SKILL.md and add an example to `demo/.jtbd/`.

## Example transcripts

We need more example transcripts for testing. If you have an anonymized interview transcript you're willing to share (no real names, companies, or identifying details), add it to `examples/` with a corresponding expected output YAML.

## Methodology

These skills encode Bob Moesta's Switch methodology. If you're proposing changes to how forces are extracted or how the timeline is structured, please reference the methodology in `docs/methodology.md` and explain your reasoning.

## Pull request template

When submitting a PR, the template asks: "Which `.jtbd/` evidence supports this change?" This is intentional. We use the JTBD framework on ourselves. If you're adding a feature, explain what user need (job) it addresses.

## Code of conduct

Be kind. Be constructive. Be specific.
