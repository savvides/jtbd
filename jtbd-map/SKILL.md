---
name: jtbd-map
description: |
  Synthesize patterns into a structured Job Map (YAML + Markdown).
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

Check for the `.jtbd/patterns/` directory. If it does not exist, tell the user to run `/jtbd-patterns` first and stop.
Ensure the `.jtbd/jobs/` directory exists.

```bash
[ -d ".jtbd/patterns" ] || { echo "Error: .jtbd/patterns/ directory not found. Run /jtbd-patterns first."; exit 1; }
mkdir -p .jtbd/jobs/
```

## Read Input

1. If the user provided a file argument, read that path.
2. If no argument is provided, look for the most recent file in `.jtbd/patterns/`. If found, ask the user to confirm using it. If not found, ask for a path.

Use the `Read` tool to inspect the selected patterns file.

## Process Data

Extract the primary job identified in the patterns file:
1. **Job Statement:** The recurring goal or outcome customers are trying to achieve.
2. **Frequency and Confidence:** Note the interview count and confidence level from the cluster.
3. **Chronological Steps:** Identify 4 to 8 sequential steps the customer takes to accomplish this job. For each step, document the observed friction point and the corresponding product opportunity.
4. **Switching Trigger:** The event or moment that escalated passive consideration into active searching.
5. **Forces Summary:** Synthesize the push, pull, anxiety, and habit forces into one concise statement each.

## Output Generation

Write two files:

### 1. YAML Data File (`.jtbd/jobs/<job-slug>.yml`)

```yaml
# Synthesized from patterns analysis

schema_version: 1
provenance:
  skill: "jtbd-map"
  version: "1.8.0.0"
  created_at: "<YYYY-MM-DD>"

job: "<Main Job Statement>"
frequency: "<N/Total> interviews"
confidence: high  # high | medium | low

steps:
  - name: "<Step 1 name>"
    friction: "<What makes this step painful or slow>"
    opportunity: "<How a product can solve this friction>"
  - name: "<Step 2 name>"
    friction: "<Friction point>"
    opportunity: "<Opportunity>"

switching_trigger: "<The critical event that forced action>"

forces_summary:
  what_pushes: "<Current tool failure or frustration>"
  what_pulls: "<Expected relief or capability with new solution>"
  what_scares: "<Migration, cost, or implementation risks>"
  what_holds: "<Comfort with existing routines and workarounds>"
```

### 2. Markdown Document (`.jtbd/jobs/<job-slug>.md`)

```markdown
# Job Map: <Main Job Statement>

**Frequency:** <N/Total> interviews | **Confidence:** <high/medium/low>

## Overview
- **Switching Trigger:** <switching_trigger>
- **Push:** <what_pushes>
- **Pull:** <what_pulls>
- **Anxiety:** <what_scares>
- **Habit:** <what_holds>

## Process Steps

| Step | Friction | Opportunity |
|---|---|---|
| <Step 1> | <Friction> | <Opportunity> |
| <Step 2> | <Friction> | <Opportunity> |
```

Tell the user where both files were saved, then list next steps:

> **Next steps:**
> - Review the Job Map steps and adjust any details
> - Run `/jtbd-brief` to generate a product brief from this Job Map
> - Run `/jtbd-forces` to visualize the four forces diagram
