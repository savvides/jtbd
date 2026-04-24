---
name: jtbd-patterns
version: 1.0.0
description: |
  Find cross-interview patterns across 3+ switch analyses in .jtbd/switches/.
  Clusters recurring jobs, identifies force patterns, surfaces evidence gaps,
  and generates actionable recommendations. Outputs structured YAML to .jtbd/patterns/.
  Use when: "find patterns", "jtbd patterns", "cross-interview", "what are the jobs".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

## Preamble

```bash
# Detect .jtbd/ directory
_JTBD_DIR=".jtbd"
_HAS_JTBD="no"
[ -d "$_JTBD_DIR" ] && _HAS_JTBD="yes"
echo "JTBD_DIR: $_HAS_JTBD"

# Detect gstack (optional integration)
_HAS_GSTACK="no"
[ -d "$HOME/.claude/skills/gstack" ] && _HAS_GSTACK="yes"
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
[ -n "$_ROOT" ] && [ -d "$_ROOT/.claude/skills/gstack" ] && _HAS_GSTACK="yes"
echo "GSTACK: $_HAS_GSTACK"

# Detect git
_HAS_GIT="no"
git rev-parse --is-inside-work-tree 2>/dev/null && _HAS_GIT="yes"
echo "GIT: $_HAS_GIT"

# Check for python3 (YAML validation)
_HAS_PYTHON="no"
command -v python3 >/dev/null 2>&1 && _HAS_PYTHON="yes"
echo "PYTHON3: $_HAS_PYTHON"

# Read manifest if .jtbd/ exists
if [ "$_HAS_JTBD" = "yes" ] && [ -f "$_JTBD_DIR/manifest.yml" ]; then
  echo "--- MANIFEST ---"
  cat "$_JTBD_DIR/manifest.yml"
  echo "--- END MANIFEST ---"
fi

# Count existing switch analyses
if [ "$_HAS_JTBD" = "yes" ] && [ -d "$_JTBD_DIR/switches" ]; then
  _SWITCH_COUNT=$(ls "$_JTBD_DIR/switches/"*.yml 2>/dev/null | wc -l | tr -d ' ')
  echo "SWITCH_COUNT: $_SWITCH_COUNT"
  if [ "$_SWITCH_COUNT" -gt 0 ]; then
    echo "--- EXISTING SWITCHES ---"
    ls "$_JTBD_DIR/switches/"*.yml
    echo "--- END SWITCHES ---"
  fi
else
  echo "SWITCH_COUNT: 0"
fi

# Check for existing patterns
if [ "$_HAS_JTBD" = "yes" ] && [ -d "$_JTBD_DIR/patterns" ]; then
  _PATTERN_COUNT=$(ls "$_JTBD_DIR/patterns/"*.yml 2>/dev/null | wc -l | tr -d ' ')
  echo "PATTERN_COUNT: $_PATTERN_COUNT"
  if [ "$_PATTERN_COUNT" -gt 0 ]; then
    echo "--- EXISTING PATTERNS ---"
    ls -t "$_JTBD_DIR/patterns/"*.yml
    echo "--- END PATTERNS ---"
  fi
else
  echo "PATTERN_COUNT: 0"
fi
```

## Gate: Minimum Data

If `JTBD_DIR` is `no`: Tell the user: "No .jtbd/ directory found. Run `/jtbd-switch` on an interview transcript first to create one." Stop.

If `SWITCH_COUNT` < 3: Tell the user: "Found {SWITCH_COUNT} switch analysis file(s). Pattern analysis needs at least 3 interviews to find meaningful signal. Run `/jtbd-switch` on {3 - SWITCH_COUNT} more transcript(s) first." Stop.

If `SWITCH_COUNT` is exactly 3: Proceed, but note: "Running with the minimum 3 interviews. Patterns will sharpen with more data."

## Read All Switch Analyses

Read every `.yml` file in `.jtbd/switches/` using the Read tool. For each file, extract and hold:

1. **Interviewee profile:** name, role, company, date
2. **Timeline:** all stages with triggers, durations, confidence levels
3. **Forces:** all push, pull, anxiety, habit entries with statements, quotes, intensity, confidence
4. **Job story:** the full job story string
5. **Evidence strength:** all scores

If a file has invalid YAML or missing required fields, skip it and warn: "Skipped {filename}: invalid format."

## Analyze Patterns

### Step 1: Cluster by Job

Compare all job stories and force patterns across interviews. Group interviews that share the same underlying job, even if the surface-level language differs.

Clustering rules:
- Two interviews share a job if they have overlapping push forces AND overlapping pull forces (similar pain, similar desired outcome)
- The job label should describe the *outcome the person wants*, not the product feature. "Get reliable numbers to leadership" not "use a dashboard"
- A single interview can belong to multiple clusters if it reveals multiple distinct jobs
- A cluster needs at least 2 interviews to be meaningful. Single-interview "clusters" go into an "emerging signals" section

For each cluster, identify:
- **Frequency:** How many of the total interviews show this job (e.g., 3/5)
- **Common push:** The shared push force across interviews in this cluster
- **Common pull:** The shared pull force across interviews in this cluster
- **Key quotes:** The strongest direct quote from each interview supporting this cluster (use verbatim quotes only, attribute with `# Name`)

### Step 2: Force Pattern Analysis

Across ALL interviews (not per-cluster), identify:

- **Strongest push:** The push force that appears with highest intensity across the most interviews
- **Strongest pull:** Same for pull
- **Strongest anxiety:** Same for anxiety
- **Strongest habit:** Same for habit

For each, include the pattern description and the supporting evidence (which interviews, what intensity).

### Step 3: Timeline Pattern Analysis

Look for patterns in the switching timeline across interviews:

- **Average passive looking duration:** How long do people sit with the pain before acting?
- **Common active-looking trigger:** What typically escalates from passive to active? (e.g., "leadership pressure" appeared in 3/3 interviews)
- **Common deciding factors:** What tips the decision? Features? People? Events?
- **Common onboarding friction:** What's hard about the actual switch?

Only include patterns that appear in 2+ interviews. Single-occurrence timeline details are noise, not signal.

### Step 4: Evidence Gaps

Identify what's MISSING from the evidence base:

- **Thin forces:** Which force category has the fewest entries or lowest confidence across interviews? (Habit is commonly underprobed.)
- **Missing perspectives:** What roles, company sizes, or use cases are NOT represented? Compare against `manifest.yml` target_user if available.
- **Low-confidence areas:** Fields frequently marked `confidence: low` or `inferred: true`
- **Missing timeline stages:** Stages frequently marked `not_discussed`
- **Score patterns:** Which `evidence_strength` dimension is consistently lowest?

### Step 5: Generate Recommendations

Based on the patterns and gaps, generate 3-5 actionable recommendations. Each recommendation should be:
- Specific enough to act on immediately
- Connected to evidence from the analysis
- Prioritized: most impactful first

Recommendation categories:
- **Positioning:** How to describe the product based on what the job actually is
- **Onboarding:** How to reduce switching anxiety based on common fears
- **Next interviews:** Who to interview next and what to probe based on evidence gaps
- **Product:** What to build or prioritize based on force intensity patterns

## Output Format

Generate a YAML file following this structure:

```yaml
# .jtbd/patterns/patterns-{YYYYMMDD}.yml
# Generated by /jtbd-patterns on {date}
# Cross-interview pattern analysis from {N} switch analyses

schema_version: 1
analysis_date: {YYYY-MM-DD}
switch_files_analyzed: {N}
files_included:
  - {filename1.yml}
  - {filename2.yml}
  - {filename3.yml}

clusters:
  - job: "{outcome-oriented job description}"
    frequency: "{N}/{total}"
    common_push: "{shared push pattern}"
    common_pull: "{shared pull pattern}"
    key_quotes:
      - "{verbatim quote}" # {Name}
      - "{verbatim quote}" # {Name}

  - job: "{second job cluster if found}"
    frequency: "{N}/{total}"
    common_push: "{shared push pattern}"
    common_pull: "{shared pull pattern}"
    key_quotes:
      - "{verbatim quote}" # {Name}

emerging_signals:
  - signal: "{pattern seen in only 1 interview but worth watching}"
    source: "{filename}"
    note: "{why this might matter with more data}"

force_patterns:
  strongest_push: "{description with evidence}"
  strongest_pull: "{description with evidence}"
  strongest_anxiety: "{description with evidence}"
  strongest_habit: "{description with evidence}"

timeline_patterns:
  avg_passive_duration: "{approximate average}"
  common_active_trigger: "{pattern}"
  common_deciding_factors:
    - "{factor 1}"
    - "{factor 2}"
  common_onboarding_friction: "{pattern}"

evidence_gaps:
  - "{specific gap with recommendation}"
  - "{specific gap with recommendation}"

recommendations:
  - "{actionable recommendation connected to evidence}"
  - "{actionable recommendation connected to evidence}"
  - "{actionable recommendation connected to evidence}"
```

### Filename Convention

Generate the filename as: `patterns-{YYYYMMDD}.yml` using today's date.

If a patterns file already exists for today, append `-2`, `-3`, etc.

## Validate Output

After generating the YAML:

If `PYTHON3` is `yes`, validate the YAML syntax:

```bash
python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" /path/to/generated/file.yml && echo "YAML_VALID" || echo "YAML_INVALID"
```

If `YAML_INVALID`: fix the YAML and re-validate. Do not proceed with broken YAML.

If `PYTHON3` is `no`: skip validation.

## Human Review

Present the analysis for review before saving using AskUserQuestion:

> **Pattern Analysis: {N} interviews**
>
> **Job Clusters:**
> {For each cluster: job label, frequency, one key quote}
>
> **Strongest Forces:**
> - Push: {strongest push pattern}
> - Pull: {strongest pull pattern}
> - Anxiety: {strongest anxiety pattern}
> - Habit: {strongest habit pattern}
>
> **Top Evidence Gaps:**
> {Top 2-3 gaps}
>
> **Top Recommendations:**
> {Top 2-3 recommendations}

Options:
- A) Looks good, save it
- B) I want to edit something (tell me what to change)
- C) Start over with different parameters

If the user chooses B, make the requested changes and re-present.

## Write and Commit

1. Create `.jtbd/patterns/` directory if it doesn't exist.

2. Write the YAML file to `.jtbd/patterns/patterns-{YYYYMMDD}.yml` using the Write tool.

3. If `GIT` is `yes` and the manifest has `auto_commit: true`:

```bash
git add .jtbd/patterns/{filename}.yml
git commit -m "jtbd: add pattern analysis across {N} interviews"
```

If the commit fails, write the file but skip the commit. Tell the user: "File written to .jtbd/patterns/{filename}.yml but not committed."

4. If `GIT` is `no`: write the file only.

5. Tell the user what was created and where:

> "Pattern analysis saved to `.jtbd/patterns/{filename}.yml`"
>
> **What this tells you:**
> - {1-2 sentence summary of the most important finding}
>
> **Next steps:**
> - Run more interviews targeting the evidence gaps above, use `/jtbd-interview` to generate a script
> - Run `/jtbd-patterns` again after new interviews to see how patterns sharpen
> - Run `/jtbd-forces` to generate an HTML forces diagram (coming soon)
> - Run `/jtbd-brief` to generate a product brief from your evidence (coming soon)
