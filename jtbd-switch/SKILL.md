---
name: jtbd-switch
version: 1.0.0
description: |
  Analyze a customer interview transcript using Moesta's Switch methodology.
  Extracts the switching timeline, four forces (push/pull/anxiety/habit),
  and a Klement-format job story. Outputs structured YAML to .jtbd/switches/.
  Use when: "analyze interview", "jtbd switch", "customer interview", "switching analysis".
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
```

## Initialize .jtbd/ (if needed)

If `JTBD_DIR` is `no`, create the `.jtbd/` directory structure before proceeding.

1. Use AskUserQuestion to gather product info:

> "No .jtbd/ directory found. I'll create one. What's your product called, and what stage are you at?"
>
> Options:
> - A) Set up now (I'll provide product name and stage)
> - B) Use defaults (product: "Unknown", stage: "pre-product")

If A: Ask for product name, one-line description, stage (pre-product / has-users / has-paying-customers), target user role, and target user context.

If B: Use defaults.

2. Create the directory structure:

```
.jtbd/
├── manifest.yml
├── .gitignore
├── raw/
└── switches/
```

3. Write `manifest.yml` with the user's answers (or defaults):

```yaml
schema_version: 1
product:
  name: "{product_name}"
  description: "{description}"
  stage: "{stage}"
target_user:
  role: "{role}"
  context: "{context}"
settings:
  auto_commit: true
  gitignore_raw: true
  evidence_threshold: 6
```

4. Write `.jtbd/.gitignore`:

```
# Raw interview transcripts contain PII - keep out of git by default
raw/
```

## Read Input

Determine the transcript source from the user's invocation:

**If a file path was provided:** Read the file using the Read tool. If file not found, tell the user and ask them to paste instead.

**If `fireflies:<id>` or a Fireflies URL was provided:** Use the `fireflies_get_transcript` MCP tool to fetch the transcript. If MCP is unavailable, tell the user: "Fireflies integration not available. Paste the transcript or provide a file path."

**If no argument:** Use AskUserQuestion:

> "Paste your interview transcript below, or provide a file path. For best results, use a transcript from a 30-60 minute customer interview where someone describes switching from one product/solution to another."

**Input validation:**
- If the transcript is less than 500 words: refuse. Tell the user: "This transcript is too short for Switch analysis. A typical Switch interview is 30-60 minutes (~5,000-10,000 words). Try a longer interview."
- If the transcript appears to be in a non-English language: warn but proceed. "This transcript appears to be in [language]. Analysis quality may vary."

Optionally save the raw transcript to `.jtbd/raw/{filename}.txt` (if `gitignore_raw: true` in manifest, which is the default).

## Extract Switch Analysis

You are now analyzing an interview transcript using Bob Moesta's Switch methodology. Your job is to extract structured data from the messy, unstructured conversation. Follow these rules precisely.

### Methodology: Moesta's Switch Framework

The Switch framework identifies why people change from one solution to another. Every switch has:

1. **A timeline** of events from first thought to consumption
2. **Four forces** that drive or resist the switch:
   - **Push of the current situation** (what's wrong with what they have now)
   - **Pull of the new solution** (what attracts them to the alternative)
   - **Anxiety of the new solution** (fears about switching)
   - **Habit of the present** (comfort with the status quo)

The switch happens when Push + Pull > Anxiety + Habit.

### Extraction Rules

**Rule 1: Every force MUST have a direct quote.** If you cannot find a verbatim quote from the transcript supporting a force, you MUST set `inferred: true` and `confidence: low`. Do NOT fabricate quotes. The quote is the evidence chain.

**Rule 2: Mark confidence on every field.** Use:
- `high`: Direct quote or explicitly stated by the interviewee
- `medium`: Paraphrased from context or partially confirmed
- `low`: Inferred from absence or implication

This same rubric applies to both forces and timeline stages. Confidence measures the source quality of the evidence, not certainty about the facts.

**Rule 3: Mark missing stages as `not_discussed`.** If a timeline stage cannot be identified from the transcript, set it to `not_discussed: true` rather than fabricating content. It is better to have gaps than hallucinations.

**Rule 4: Evidence scores are directional, not precise.** A 3/10 vs 8/10 is meaningful. A 6/10 vs 7/10 is noise. Score honestly based on the rubric. Include a comment in the YAML: `# Note: scores are directional (3 vs 8 meaningful, 6 vs 7 is noise)`

**Rule 5: For long transcripts (>20,000 words),** use a two-pass approach within your reasoning: first identify timeline events and key quotes, then analyze forces from the extracted material.

### Output Format

Generate a YAML file following this exact structure. Every field shown here must be present in the output (use `not_discussed: true` for stages you can't identify, `~` for missing quotes, `inferred: true` for unsupported forces).

```yaml
# .jtbd/switches/{first-name}-{role-slug}-{YYYYMMDD}.yml
# Generated by /jtbd-switch on {date}
# Note: evidence scores are directional (3 vs 8 meaningful, 6 vs 7 is noise)

interviewee:
  name: "{First Name}"
  role: "{Role Title}"
  company: "{Company Name} ({size if mentioned})"
  date: "{YYYY-MM-DD}"

timeline:
  first_thought:
    when: "{approximate time}"
    trigger: "{what event or realization started the process}"
    quote: "{verbatim quote from transcript}"
    confidence: high  # high | medium | low
  passive_looking:
    duration: "{how long}"
    actions: ["{action 1}", "{action 2}"]
    confidence: medium
  active_looking:
    duration: "{how long}"
    actions: ["{action 1}", "{action 2}"]
    trigger: "{what escalated from passive to active}"
    confidence: high
  deciding:
    chose: "{what they chose}"
    deciding_factors: ["{factor 1}", "{factor 2}"]
    confidence: high
  consuming:
    onboarding: "{how the transition went}"
    friction: "{what was hard about switching}"
    confidence: medium

# intensity: 1-10, how strongly this force influenced the switching decision
# (10 = dominant driver, 1 = barely relevant)
# confidence: high (direct quote), medium (paraphrased), low (inferred)
# inferred: true only when no direct quote supports the force
forces:
  push:
    - statement: "{one-sentence description of the push force}"
      quote: "{verbatim quote}"
      intensity: 8
      confidence: high
  pull:
    - statement: "{one-sentence description of the pull force}"
      quote: "{verbatim quote}"
      intensity: 7
      confidence: high
  anxiety:
    - statement: "{one-sentence description of the anxiety}"
      quote: "{verbatim quote}"
      intensity: 5
      confidence: medium
  habit:
    - statement: "{one-sentence description of the habit}"
      quote: "{verbatim quote}"
      intensity: 4
      confidence: medium

job_story: "When {situation}, I want to {motivation}, so I can {expected outcome}."

evidence_strength:
  direct_quotes: 7    # 1-10 per rubric
  behavioral_specificity: 8
  timeline_clarity: 6
  overall: 6          # minimum of the three scores above
```

### Filename Convention

Generate the filename as: `{first-name}-{role-slug}-{YYYYMMDD}.yml`
- `first-name`: lowercase, alphanumeric + hyphens only
- `role-slug`: lowercase role with spaces replaced by hyphens
- `YYYYMMDD`: interview date (use today's date if not mentioned)

If the file already exists, append `-2`, `-3`, etc.

## Validate Output

After generating the YAML:

If `PYTHON3` is `yes`, validate the YAML syntax:

```bash
python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" /path/to/generated/file.yml && echo "YAML_VALID" || echo "YAML_INVALID"
```

If `YAML_INVALID`: regenerate the output. Do not proceed with broken YAML.

If `PYTHON3` is `no`: skip validation (Claude's output is usually valid YAML, and the human review step catches issues).

## Human Review

This step is NOT optional. Always present the analysis for review before committing.

Use AskUserQuestion to present a summary:

> **Switch Analysis Summary for {Name}, {Role}**
>
> **Timeline:** First thought ({when}) -> Passive looking ({duration}) -> Active looking ({duration}) -> Decided on {choice} -> Consuming ({onboarding summary})
>
> **Forces:**
> - Push ({count}): {strongest push statement} (intensity: {n})
> - Pull ({count}): {strongest pull statement} (intensity: {n})
> - Anxiety ({count}): {strongest anxiety statement} (intensity: {n})
> - Habit ({count}): {strongest habit statement} (intensity: {n})
>
> **Job story:** "{job_story}"
>
> **Evidence strength:** {overall}/10
>
> **Note:** This file contains interview data including names, companies, and direct quotes. Make sure your repo is private, or redact sensitive information before committing to a public repo.

Options:
- A) Looks good, save it
- B) I want to edit something (tell me what to change)
- C) Start over with this transcript

If the user chooses B, make the requested changes and re-present.

### Quality Warning

If `evidence_strength.overall` < 5, add this warning to the AskUserQuestion:

> **Warning:** Evidence strength is low ({overall}/10). This interview may not have been a Switch interview, or the transcript is missing key moments. Consider re-interviewing using a `/jtbd-interview` script (coming soon).

## Write and Commit

1. Write the YAML file to `.jtbd/switches/{filename}.yml` using the Write tool.

2. If `GIT` is `yes` and the manifest has `auto_commit: true`:

```bash
git add .jtbd/switches/{filename}.yml
git commit -m "jtbd: add switch analysis for {Name} ({Role})"
```

If the commit fails (dirty tree, hooks, etc.), write the file but skip the commit. Tell the user: "File written to .jtbd/switches/{filename}.yml but not committed. Run `git add` and `git commit` manually."

3. If `GIT` is `no`: write the file only. Tell the user: "File written to .jtbd/switches/{filename}.yml. No git repo detected, so the file was not committed."

4. Tell the user what was created and where:

> "Switch analysis saved to `.jtbd/switches/{filename}.yml`"
>
> **Next steps:**
> - Do more interviews and run `/jtbd-switch` on each one
> - After 3+ interviews, run `/jtbd-patterns` to find cross-interview patterns (coming soon)
> - Run `/jtbd-interview` to generate a customized interview script
