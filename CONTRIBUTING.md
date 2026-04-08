# Contributing to jtbd

Thanks for wanting to contribute. Here's how.

## Adding a new skill

Each skill is a directory with a single `SKILL.md` file:

```
jtbd-yourskill/
└── SKILL.md
```

The `SKILL.md` needs:

1. **YAML frontmatter** with `name`, `version`, `description`, and `allowed-tools`
2. **A preamble bash block** that detects `.jtbd/` and gstack
3. **Clear instructions** for Claude on what to extract/generate
4. **An example output** showing the exact expected format
5. **A human review step** using AskUserQuestion before writing files

Look at `jtbd-switch/SKILL.md` or `jtbd-interview/SKILL.md` as reference implementations.

## YAML schema

All `.jtbd/` files use `schema_version: 1`. If you're adding a skill that writes new file types to `.jtbd/`, document the schema in your SKILL.md and add an example to `demo/.jtbd/`.

## Example transcripts

We need more example transcripts for testing. If you have an anonymized interview transcript you're willing to share (no real names, companies, or identifying details), add it to `examples/` with a corresponding expected output YAML.

## Methodology

These skills encode Bob Moesta's Switch methodology. If you're proposing changes to how forces are extracted or how the timeline is structured, please reference the methodology in `docs/methodology.md` and explain your reasoning.

## Pull request template

When submitting a PR, the template asks: "Which `.jtbd/` evidence supports this change?" This is intentional. We use the JTBD framework on ourselves. If you're adding a feature, explain what user need (job) it addresses.

## Code of conduct

Be kind. Be constructive. Be specific.
