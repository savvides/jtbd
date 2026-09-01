---
name: jtbd-forces
description: |
  Generate an HTML diagram of the four forces driving a switch.
  Accepts either a single interview file (.jtbd/switches/*.yml) or an aggregate patterns file (.jtbd/patterns/*.yml).
  Outputs a standalone HTML file to .jtbd/forces/.
  Use when: "draw forces", "jtbd forces", "forces diagram", "forces visualization".
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

## Preamble

Check for the `.jtbd/` directory. If it does not exist, tell the user to run `/jtbd-switch` or `/jtbd-patterns` first and stop.
Ensure the `.jtbd/forces/` directory exists.

```bash
[ -d ".jtbd" ] || { echo "Error: .jtbd/ directory not found. Run /jtbd-switch or /jtbd-patterns first."; exit 1; }
mkdir -p .jtbd/forces/
```

## Read Input

1. If the user provided a file argument, read that path.
2. If no argument is provided, ask the user to provide the path to a switch file (`.jtbd/switches/*.yml`) or a patterns file (`.jtbd/patterns/*.yml`).

Use the `Read` tool to inspect the contents of the file.

## Process Data

Determine the input file type:
- **Switch File:** Extract `interviewee` information and the list of forces under `push`, `pull`, `anxiety`, and `habit`. For each force item, extract `statement`, `intensity` (1-10), `confidence`, and `quote` (if present).
- **Pattern File:** Extract the clusters and aggregated force patterns across interviews.

## Generate HTML

Generate a single, self-contained HTML file without external CSS or JS dependencies.

### Layout & Visual Design Specifications
- **Grid Layout:** 2 columns x 2 rows representing the Four Forces:
  - **Top Left (Push):** Forces of the current situation driving away from status quo (arrow pointing right).
  - **Bottom Left (Pull):** Allure of the new solution attracting the buyer (arrow pointing right).
  - **Top Right (Anxiety):** Uncertainties and fears about the new solution (arrow pointing left).
  - **Bottom Right (Habit):** Inertia and comfort with existing routines (arrow pointing left).
- **Center Axis:** A clear visual divider indicating the switching threshold: Progress (Push + Pull) versus Friction (Anxiety + Habit).
- **Card Content:** Each force card displays:
  - Title and force name
  - Intensity score badge (e.g. `8/10`)
  - Summary statement
  - Direct quote excerpt in italics (or marked `[Inferred from interview context]` if no quote is present)
  - Confidence tag (`high`, `medium`, or `low`)
- **Typography & Styling:** Clean sans-serif system fonts (`system-ui, -apple-system, sans-serif`), clear contrast, subtle borders, and modern card styling.

## Output

Write the generated HTML to `.jtbd/forces/<filename-base>.html` using the `Write` tool.

Tell the user where the file was saved, then list next steps:

> **Next steps:**
> - Open the HTML file in a browser to inspect the forces visualization
> - Run `/jtbd-map` to synthesize patterns into a Job Map
> - Run `/jtbd-brief` to generate a product brief from your evidence
