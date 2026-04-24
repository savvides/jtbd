---
name: jtbd-pipeline
version: 1.0.0
description: |
  Run the full JTBD analysis pipeline on a batch of interview transcripts.
  Analyzes each transcript into a Switch analysis, then finds cross-interview
  patterns. Accepts a directory of transcript files or Fireflies meeting IDs.
  Use when: "analyze all interviews", "jtbd pipeline", "batch analysis", "process transcripts".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
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
else
  echo "SWITCH_COUNT: 0"
fi

# Detect jtbd skill locations
_JTBD_SKILLS=""
if [ -d "$HOME/.claude/skills/jtbd" ]; then
  _JTBD_SKILLS="$HOME/.claude/skills/jtbd"
elif [ -n "$_ROOT" ] && [ -f "$_ROOT/jtbd-switch/SKILL.md" ]; then
  _JTBD_SKILLS="$_ROOT"
fi
echo "JTBD_SKILLS: ${_JTBD_SKILLS:-not found}"
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

## Discover Inputs

Determine the transcript source from the user's invocation:

**If a directory path was provided:** Glob for transcript files in that directory.

```bash
ls {directory}/*.txt {directory}/*.md 2>/dev/null
```

Count the files found. If zero, tell the user: "No .txt or .md files found in {directory}." and stop.

**If Fireflies meeting IDs were provided** (format: `fireflies:id1,id2,id3`): Use the `fireflies_get_transcript` MCP tool to fetch each transcript. If MCP is unavailable, tell the user and ask them to provide file paths instead.

**If no argument:** Use AskUserQuestion:

> "Where are your interview transcripts? Provide a directory path containing .txt or .md files, or paste Fireflies meeting IDs."
>
> Options:
> - A) I'll provide a directory path
> - B) I have Fireflies meeting IDs
> - C) I'll paste transcripts directly (one at a time)

**List the discovered transcripts** for the user:

> "Found {N} transcript(s):"
> - {filename1} ({word_count} words)
> - {filename2} ({word_count} words)
> ...

If any transcript is under 500 words, warn: "{filename} is very short ({word_count} words). Switch analysis works best with 5,000-10,000 word transcripts from 30-60 minute interviews. Include it anyway?"

## Run Switch Analysis on Each Transcript

For each transcript, run the `/jtbd-switch` analysis. This is the core loop.

### Execution Strategy

**If 3 or fewer transcripts:** Run sequentially. For each transcript:
1. Read the transcript file
2. Follow the `/jtbd-switch` extraction rules (from `jtbd-switch/SKILL.md`):
   - Extract the switching timeline (first thought, passive looking, active looking, deciding, consuming)
   - Extract the four forces (push, pull, anxiety, habit) with verbatim quotes and intensity scores
   - Generate a job story in Klement format
   - Score evidence strength
3. Write the YAML to `.jtbd/switches/{filename}.yml`
4. Validate YAML if python3 is available
5. Report: "Analyzed {name} ({role}): {job_story_summary}"

**If 4 or more transcripts:** Use the Agent tool to parallelize. Dispatch up to 4 agents concurrently, each running switch analysis on a different transcript.

Each agent prompt should include:
- The full transcript content
- The extraction rules from the "Extract Switch Analysis" section of `jtbd-switch/SKILL.md` (methodology, extraction rules, output format, filename convention)
- The `.jtbd/switches/` output path
- Instructions to write the YAML file and report the result

After all agents complete, verify each output file exists and is valid YAML.

### Progress Reporting

After each transcript is analyzed (sequential or parallel), report progress:

> "Progress: {completed}/{total} transcripts analyzed"
> - {name} ({role}): "{one-line job story}" — evidence: {overall}/10

### Error Handling

If a transcript fails analysis (too short, not an interview, invalid content):
- Skip it with a warning: "Skipped {filename}: {reason}"
- Continue with remaining transcripts
- Include the skip in the final summary

## Human Review Gate

After all switch analyses are complete, present a summary for review:

> **Pipeline: Switch Analysis Complete**
>
> **Analyzed:** {N} transcripts → {M} switch files
> **Skipped:** {K} (if any, list reasons)
>
> **Interviewees:**
> {For each: name, role, company, evidence score}
>
> **Job Stories:**
> {For each: the job story}
>
> **Note:** These files contain interview data including names, companies, and direct quotes. Make sure your repo is private, or redact sensitive information before committing.

Options:
- A) Looks good, continue to pattern analysis
- B) I want to review/edit individual analyses first
- C) Stop here (I'll run /jtbd-patterns manually later)

If B: Let the user specify which files to review. Present each for editing. Then re-present the summary.

If C: Commit the switch files and stop.

## Run Pattern Analysis

If the user approved continuing AND there are 3+ switch analyses total (including any pre-existing ones):

1. Read ALL switch analysis files in `.jtbd/switches/` (not just the new ones)
2. Follow the `/jtbd-patterns` analysis workflow:
   - Cluster by job (overlapping push + pull forces)
   - Analyze force patterns across all interviews
   - Analyze timeline patterns
   - Identify evidence gaps
   - Generate recommendations
3. Write the patterns YAML to `.jtbd/patterns/patterns-{YYYYMMDD}.yml`
4. Validate YAML if python3 is available

If fewer than 3 total switch analyses: Skip patterns with a note: "Only {N} switch analyses available. Pattern analysis needs 3+. Run more interviews and then run `/jtbd-patterns`."

## Commit and Summary

1. Stage all new files:

```bash
git add .jtbd/switches/*.yml .jtbd/patterns/*.yml .jtbd/manifest.yml .jtbd/.gitignore
```

2. If `GIT` is `yes` and the manifest has `auto_commit: true`:

```bash
git commit -m "jtbd: pipeline analysis of {N} interviews"
```

3. Present the final summary:

> **JTBD Pipeline Complete**
>
> **Input:** {N} transcripts from {source}
> **Switch analyses:** {M} created, {K} skipped
> **Total in .jtbd/switches/:** {total} (including pre-existing)
> **Patterns:** {generated | skipped (need 3+)}
>
> **Key Findings:**
> {If patterns were generated:}
> - **Primary job:** "{top cluster job}" ({frequency})
> - **Strongest push:** {description}
> - **Biggest evidence gap:** {description}
> - **Top recommendation:** {recommendation}
>
> **Next steps:**
> - Review individual switch files in `.jtbd/switches/`
> - Run `/jtbd-interview` to generate scripts targeting evidence gaps
> - Run `/jtbd-forces` to generate a visual forces diagram (coming soon)
> - Run `/jtbd-brief` to generate a product brief from your evidence (coming soon)
> - If using gstack: run `/office-hours` to turn your brief into a design doc
