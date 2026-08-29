---
name: jtbd-brief
version: 1.0.0
description: |
  Drafts a JTBD-native product brief from Job Map data.
  Accepts a Job Map YAML file (.jtbd/jobs/*.yml).
  Outputs to .jtbd/briefs/.
  Use when: "product brief", "jtbd brief", "write prd".
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

## Preamble

Check for the `.jtbd/jobs/` directory. If it doesn't exist, tell the user they need to run `/jtbd-map` first and exit.
Make sure the `.jtbd/briefs/` directory exists.

```bash
[ -d ".jtbd/jobs" ] || { echo "Error: .jtbd/jobs/ directory not found. Run /jtbd-map first."; exit 1; }
mkdir -p .jtbd/briefs/
```

## Read Input

1. If the user provided an argument, use that file path.
2. If no argument is provided, ask the user to provide the path to a Job Map YAML file (in `.jtbd/jobs/`).

Use the `Read` tool to read the Job Map file. Ask the user if they also want to include context from a specific pattern file; if yes, read that too.

## Process Data

Draft a "JTBD-Native" Product Brief. The brief must explicitly link proposed features or interventions back to the friction points identified in the Job Map.

Structure the brief exactly like this:
```markdown
# Product Brief: [Feature/Project Name]

## 1. The Job
[What the customer is trying to achieve]

## 2. The Forces
[What is pushing/pulling them, and what anxieties/habits must be overcome]

## 3. Timeline Interventions
[Where in the customer's journey the product should intercept them]

## 4. Map Opportunities
[Specific feature proposals directly linked to the friction points in the Job Map]
```

## Output

Write the generated Markdown to `.jtbd/briefs/[feature-slug].md` using the `Write` tool.

Tell the user where the file was saved, then:

> **Next steps:**
> - Check every feature proposal traces back to a friction point in the Job Map
> - Run more interviews if the brief leans on thin evidence
> - If using gstack: run `/office-hours` to turn this brief into a design doc

