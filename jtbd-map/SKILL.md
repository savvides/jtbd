<!-- jtbd-map/SKILL.md -->
---
name: jtbd-map
version: 1.0.0
description: |
  Synthesizes patterns into a structured Job Map (YAML + Markdown).
  Accepts a patterns file (.jtbd/patterns/*.yml).
  Outputs to .jtbd/jobs/.
  Use when: "create job map", "jtbd map", "job mapping".
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

## Preamble

Check for the `.jtbd/` directory.
Make sure the `.jtbd/jobs/` directory exists.

```bash
[ -d ".jtbd/patterns" ] || { echo "Error: .jtbd/patterns/ directory not found. Run /jtbd-patterns first."; exit 1; }
mkdir -p .jtbd/jobs/
```

## Read Input

1. If the user provided an argument, use that file path.
2. If no argument is provided, look for the most recent file in `.jtbd/patterns/`. If found, ask the user to confirm using it. If not found, ask for a path.

Use the `Read` tool to read the patterns file.

## Process Data

Instruct the LLM to deduce the chronological steps of the dominant job identified in the patterns file. For each step, identify friction points and propose high-level opportunities based on the clustered jobs, emerging signals, and timeline patterns.

## Output Generation

You must generate TWO files:

**1. YAML Data File:**
Write to `.jtbd/jobs/[job-slug].yml`. Format:
```yaml
job: "[Main Job Statement]"
steps:
  - name: "[Step 1]"
    friction: "[Friction]"
    opportunity: "[Opportunity]"
  # ... more steps
```

**2. Markdown Visual File:**
Write to `.jtbd/jobs/[job-slug].md`. Format as a clean document with a Markdown table for the steps:
```markdown
# Job Map: [Main Job Statement]

| Step | Friction | Opportunity |
|---|---|---|
| [Step 1] | [Friction] | [Opportunity] |
```

Inform the user where both files were saved.