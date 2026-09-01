---
name: jtbd-brief
description: |
  Draft a JTBD-native product brief from Job Map data.
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

Check for the `.jtbd/jobs/` directory. If it does not exist, tell the user to run `/jtbd-map` first and stop.
Ensure the `.jtbd/briefs/` directory exists.

```bash
[ -d ".jtbd/jobs" ] || { echo "Error: .jtbd/jobs/ directory not found. Run /jtbd-map first."; exit 1; }
mkdir -p .jtbd/briefs/
```

## Read Input

1. If the user provided an argument, read that file path.
2. If no argument is provided, look for files in `.jtbd/jobs/`. If found, ask the user which one to use. If not found, ask for a path.

Use the `Read` tool to read the Job Map YAML file.

## Process Data

Draft a structured product brief grounded in the Job Map data:
- **1. The Job:** The core progress the customer is seeking (`job`, `frequency`, `confidence`).
- **2. The Forces:** The four forces from `forces_summary` (`what_pushes`, `what_pulls`, `what_scares`, `what_holds`).
- **3. Timeline Interventions:** Where and when the product intervenes in the customer journey (`switching_trigger` and early friction steps).
- **4. Map Opportunities:** Explicit feature and product proposals directly tied to each friction point in `steps`.

## Output Generation

Write the product brief to `.jtbd/briefs/<feature-slug>.md` using the `Write` tool:

```markdown
# Product Brief: <Feature/Project Name>

**Target Job:** <job>
**Evidence Basis:** <frequency> (<confidence> confidence)

## 1. The Job
<Description of the job to be done, the customer's goal, and why existing alternatives fall short>

## 2. The Forces
- **Push:** <what_pushes>
- **Pull:** <what_pulls>
- **Anxiety:** <what_scares>
- **Habit:** <what_holds>

## 3. Timeline Interventions
- **Trigger Event:** <switching_trigger>
- **Intervention Strategy:** <How the product intercepts the user when urgency peaks>

## 4. Product Opportunities & Requirements
<For each step in the Job Map, list the friction and the concrete solution requirement>

| Job Step | Customer Friction | Proposed Capability |
|---|---|---|
| <Step 1> | <Friction 1> | <Feature / Capability> |
| <Step 2> | <Friction 2> | <Feature / Capability> |
```

Tell the user where the file was saved, then list next steps:

> **Next steps:**
> - Review the feature proposals against customer interview quotes
> - Share this brief with engineering and design
> - Run more interviews if any section relies on low-confidence evidence

