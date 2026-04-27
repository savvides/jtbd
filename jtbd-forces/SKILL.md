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
