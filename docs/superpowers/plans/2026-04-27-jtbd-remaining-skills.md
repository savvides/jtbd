# Final JTBD Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the three remaining JTBD skills (`/jtbd-forces`, `/jtbd-map`, and `/jtbd-brief`) to complete the package.

**Architecture:** We are creating three independent skills. Each skill requires a Claude Code command file in `.claude/commands/` and a corresponding `SKILL.md` file in its own directory (`jtbd-forces/`, `jtbd-map/`, `jtbd-brief/`). The skills rely on Claude Code's built-in tools (Read, Write, Bash, AskUserQuestion).

**Tech Stack:** Markdown (for skills and outputs), HTML/CSS (for the forces diagram), YAML (for data parsing/generation).

---

### Task 1: Setup `/jtbd-forces` Command and Skill

**Files:**
- Create: `.claude/commands/jtbd-forces.md`
- Create: `jtbd-forces/SKILL.md`

- [ ] **Step 1: Create the command shortcut**

```markdown
<!-- .claude/commands/jtbd-forces.md -->
Read the skill definition at jtbd-forces/SKILL.md and execute it exactly as specified. Pass through any arguments: $ARGUMENTS
```

- [ ] **Step 2: Write the `jtbd-forces` skill definition**

```markdown
<!-- jtbd-forces/SKILL.md -->
---
name: jtbd-forces
version: 1.0.0
description: |
  Generates an HTML diagram of the four forces driving a switch.
  Accepts either a single interview file (.jtbd/switches/*.yml) or an aggregate patterns file (.jtbd/patterns/*.yml).
  Outputs a standalone HTML file to .jtbd/forces/.
  Use when: "draw forces", "jtbd forces", "forces diagram".
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

## Preamble

Check for the `.jtbd/` directory. If it doesn't exist, tell the user they need to run `/jtbd-switch` or `/jtbd-patterns` first and exit.
Make sure the `.jtbd/forces/` directory exists.

```bash
[ -d ".jtbd" ] || { echo "Error: .jtbd/ directory not found. Run /jtbd-switch first."; exit 1; }
mkdir -p .jtbd/forces/
```

## Read Input

Determine the input file:
1. If the user provided an argument, use that file path.
2. If no argument is provided, ask the user to provide the path to a switch file or a patterns file.

Use the `Read` tool to read the contents of the provided file.

## Process Data

Determine the type of file based on its structure:
- **Switch File:** If the file contains `interviewee:` and `forces:`, extract the `push`, `pull`, `anxiety`, and `habit` quotes and intensities.
- **Pattern File:** If the file contains `clusters:` and `force_patterns:`, extract the strongest push, pull, anxiety, and habit patterns.

## Generate HTML

Generate a standalone HTML file. It must not rely on external CSS/JS. Use Flexbox or CSS Grid to create a visual layout matching Moesta's methodology:
- Left side: Push (top) and Pull (bottom) arrows pointing right.
- Right side: Anxiety (top) and Habit (bottom) arrows pointing left.

Include the extracted quotes/patterns in the respective quadrants.

## Output

Write the generated HTML to `.jtbd/forces/[filename-base].html` using the `Write` tool. (e.g., if input was `sarah-ops.yml`, output is `sarah-ops.html`).
Inform the user where the file was saved.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/jtbd-forces.md jtbd-forces/SKILL.md
git commit -m "feat: add /jtbd-forces command and skill definition"
```

### Task 2: Setup `/jtbd-map` Command and Skill

**Files:**
- Create: `.claude/commands/jtbd-map.md`
- Create: `jtbd-map/SKILL.md`

- [ ] **Step 1: Create the command shortcut**

```markdown
<!-- .claude/commands/jtbd-map.md -->
Read the skill definition at jtbd-map/SKILL.md and execute it exactly as specified. Pass through any arguments: $ARGUMENTS
```

- [ ] **Step 2: Write the `jtbd-map` skill definition**

```markdown
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
[ -d ".jtbd" ] || { echo "Error: .jtbd/ directory not found."; exit 1; }
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
```

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/jtbd-map.md jtbd-map/SKILL.md
git commit -m "feat: add /jtbd-map command and skill definition"
```

### Task 3: Setup `/jtbd-brief` Command and Skill

**Files:**
- Create: `.claude/commands/jtbd-brief.md`
- Create: `jtbd-brief/SKILL.md`

- [ ] **Step 1: Create the command shortcut**

```markdown
<!-- .claude/commands/jtbd-brief.md -->
Read the skill definition at jtbd-brief/SKILL.md and execute it exactly as specified. Pass through any arguments: $ARGUMENTS
```

- [ ] **Step 2: Write the `jtbd-brief` skill definition**

```markdown
<!-- jtbd-brief/SKILL.md -->
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

Check for `.jtbd/` directory.
Make sure the `.jtbd/briefs/` directory exists.

```bash
[ -d ".jtbd" ] || { echo "Error: .jtbd/ directory not found."; exit 1; }
mkdir -p .jtbd/briefs/
```

## Read Input

1. If the user provided an argument, use that file path.
2. If no argument is provided, ask the user to provide the path to a Job Map YAML file (in `.jtbd/jobs/`).

Use the `Read` tool to read the Job Map file. Ask the user if they also want to include context from a specific pattern file; if yes, read that too.

## Process Data

Instruct the LLM to draft a "JTBD-Native" Product Brief. The brief must explicitly link proposed features or interventions back to the friction points identified in the Job Map.

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
Inform the user where the file was saved.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/jtbd-brief.md jtbd-brief/SKILL.md
git commit -m "feat: add /jtbd-brief command and skill definition"
```

### Task 4: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update the Available Skills table**

Edit `README.md` to change the "Status" of the final three skills from "Coming soon" to "Available".

```markdown
| `/jtbd-forces` | **Available** | Create an HTML forces diagram. |
| `/jtbd-map` | **Available** | Synthesize your patterns into a full job map. |
| `/jtbd-brief` | **Available** | Draft a product brief straight from the .jtbd/ data. |
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README to reflect all skills are available"
```
