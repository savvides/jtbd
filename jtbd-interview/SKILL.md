---
name: jtbd-interview
version: 1.0.0
description: |
  Generate a customized Switch interview script based on your product context
  and existing evidence gaps. Outputs a ready-to-use markdown guide with
  Moesta's timeline reconstruction questions and force-probing techniques.
  Use when: "interview script", "jtbd interview", "interview guide", "how to interview".
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

## Gather Context

### Read existing evidence

If `SWITCH_COUNT` > 0, read ALL existing switch analysis files from `.jtbd/switches/`. Analyze them for:

1. **Force gaps**: Which forces are thin across interviews? (e.g., habit forces often underprobed)
2. **Timeline gaps**: Which timeline stages are frequently `not_discussed`?
3. **Low-confidence areas**: Fields marked `confidence: low` or `inferred: true`
4. **Missing perspectives**: What roles/personas have been interviewed vs. not?
5. **Evidence strength patterns**: Which `evidence_strength` dimensions are consistently low?

Store these gaps — they will be used to customize the interview script.

### Determine interview context

Use AskUserQuestion:

> "Who are you interviewing, and what's the context?"

Options:
- A) Someone who recently switched TO our product
- B) Someone who recently switched AWAY from our product (churned)
- C) Someone who recently switched between competitors (not our product)
- D) Someone who is currently evaluating / hasn't decided yet

Then ask:

> "What do you already know about this person?"

Options:
- A) I have their name and role (I'll provide details)
- B) I know their general persona but not specific details
- C) Nothing yet — generate a general script

If A: Collect name, role, company (optional), and any known context about their situation.

If B: Collect the persona description.

## Generate the Interview Script

Generate a markdown interview script customized to the context gathered above. The script must follow Moesta's Switch methodology precisely.

### Script Structure

The script has 6 sections. Each section has:
- A purpose statement (why you're asking these questions)
- The questions themselves
- Interviewer notes in blockquotes (tips, red flags, follow-up cues)

#### Section 1: Opening & Rapport (2-3 minutes)

Purpose: Make the interviewee comfortable. Establish that there are no wrong answers. You're interested in their story, not evaluating them.

Generate 2-3 opening questions. These should be warm, easy, and related to their role. Example:

```markdown
## 1. Opening

**Purpose:** Build rapport. No wrong answers — you want their story.

- "Tell me a bit about your role at {company}. What does a typical day look like?"
- "How long have you been in this role?"

> **Interviewer note:** Keep this under 3 minutes. You're warming up, not interrogating. Match their energy. If they're terse, be terse. If they're chatty, let them talk.
```

#### Section 2: Set the Scene (3-5 minutes)

Purpose: Establish what they were using before (the "old way") and get them to describe their world before the switch. This is critical context.

Generate 3-4 questions. Key technique: ask about the **situation**, not opinions.

```markdown
## 2. The Old Way

**Purpose:** Understand their world before the switch. What were they using? How did it work?

- "Before you started using {new solution}, what were you using to {do the job}?"
- "Walk me through how that worked on a typical {day/week/month}."
- "How long had you been doing it that way?"

> **Interviewer note:** Listen for workarounds. People compensate for bad tools without realizing it. "Oh, I had a spreadsheet for that" = habit force. Get specific: which spreadsheet? How often? Who maintained it?
```

#### Section 3: Timeline Reconstruction (10-15 minutes)

Purpose: This is the core of the Switch interview. Reconstruct the timeline by working **backward** from the decision.

Generate questions for each timeline stage. Start with the decision and work back to the first thought.

**Deciding (start here):**
```markdown
## 3. The Timeline

### 3a. The Decision

**Purpose:** Anchor on the specific moment they decided. Work backward from here.

- "Take me back to the moment you decided to go with {new solution}. Where were you? What was happening?"
- "What specifically tipped you over the edge? Was there a final straw?"
- "Were you considering anything else at that point? What were the other options?"
- "Who else was involved in the decision?"

> **Interviewer note:** Push for specificity. "When was that exactly?" "Was it before or after [event]?" You want dates, locations, people. If they say "we just decided," probe: "Was there a meeting? An email? A conversation?" The decision always has a moment.
```

**Active Looking:**
```markdown
### 3b. Active Looking

- "Before you decided, what did the search look like? Were you actively comparing options?"
- "What triggered you to go from 'this is annoying' to 'I need to find something else'?"
- "What did you Google? Who did you ask? What demos did you sit through?"
- "How long did this phase last?"

> **Interviewer note:** The trigger from passive to active is gold. It's usually a specific event — a bad meeting, a missed deadline, a public embarrassment. Probe until you get the story.
```

**Passive Looking:**
```markdown
### 3c. Passive Looking

- "Before you were actively searching, were you aware that alternatives existed?"
- "How did you first hear about {new solution} or tools like it?"
- "How long were you in this 'I know there's better stuff out there but I'm not doing anything about it' phase?"

> **Interviewer note:** This phase can last months or years. People tolerate a lot. The duration tells you how strong the habit forces are.
```

**First Thought:**
```markdown
### 3d. First Thought

- "Can you remember the very first time you thought 'this isn't working'? What happened?"
- "Was there a specific event, or was it a slow build?"

> **Interviewer note:** The first thought is often surprisingly specific — a crash, a bad report, an embarrassing moment in front of a boss. If they say "I don't remember," try: "Was it before or after [major event]?" to jog memory.
```

#### Section 4: Force Probing (10-15 minutes)

Purpose: Now that the timeline is established, probe each force explicitly. The timeline questions will have surfaced some forces naturally — this section fills gaps.

**Push questions:**
```markdown
## 4. The Four Forces

### 4a. Push — What was broken?

- "What was the most frustrating thing about {old solution}?"
- "Tell me about a specific time it let you down."
- "What did that cost you — time, money, reputation, stress?"

> **Interviewer note:** Push forces must be specific events, not vague feelings. "It was slow" → "Tell me about a time the slowness actually caused a problem." Get the story, the stakes, the people involved.
```

**Pull questions:**
```markdown
### 4b. Pull — What attracted you?

- "What was the first thing about {new solution} that caught your attention?"
- "When you imagined using it, what did you picture being different?"
- "Was there a specific feature or moment in the demo/trial that made you think 'this is it'?"

> **Interviewer note:** Pull is about the *imagined future*, not features. "Real-time dashboards" is a feature. "My CEO can get his own numbers without asking me" is pull. Keep asking "why does that matter?" until you hit the emotional payoff.
```

**Anxiety questions:**
```markdown
### 4c. Anxiety — What scared you?

- "What almost stopped you from switching?"
- "What was the scariest part of the transition?"
- "Was there a moment where you almost backed out?"
- "What could have gone wrong?"

> **Interviewer note:** People don't volunteer anxiety. You have to ask directly. Silence after the question is fine — let them think. Common anxieties: data loss, team resistance, looking foolish, wasted money, learning curve. If they say "nothing," try: "If you had to name one risk, even a small one..."
```

**Habit questions:**
```markdown
### 4d. Habit — What kept you on the old way?

- "Was there anything about {old solution} that you actually liked or would miss?"
- "Did anyone on your team resist the change? Why?"
- "Were there workarounds you'd built that you had to give up?"
- "What would have happened if you'd just... kept doing what you were doing?"

> **Interviewer note:** Habit is the most underprobed force. People build elaborate workarounds and forget they're workarounds. "My analyst had a whole process" = someone's entire job was compensating for a broken tool. That's a habit force AND a push force.
```

#### Section 5: The Job Story (2-3 minutes)

Purpose: Validate your understanding by reflecting back what you heard.

```markdown
## 5. Reflect Back

**Purpose:** Confirm you understood the story correctly.

- "Let me play this back to you. It sounds like [summarize the situation], and you wanted [motivation], so you could [outcome]. Does that sound right?"
- "Is there anything I'm missing?"

> **Interviewer note:** This is your job story draft. If they correct you, update it. Their correction is often more precise than your summary. Write it down verbatim.
```

#### Section 6: Wrap-up (2-3 minutes)

```markdown
## 6. Wrap-up

- "If you could go back and give yourself advice at the start of this process, what would you say?"
- "Is there anything I should have asked that I didn't?"
- "Thanks — this was incredibly helpful."

> **Interviewer note:** The "advice to yourself" question often surfaces the strongest anxiety or habit force. The "anything I missed" question catches things you didn't know to ask about.
```

### Customization Rules

Apply these customizations based on the context gathered:

**If interview context is "switched AWAY" (churned):**
- Flip the framing: the "old way" is YOUR product, the "new solution" is whatever they switched to
- Add questions: "What would have kept you?" and "When did you first think about leaving?"
- The push forces are about YOUR product's failures — this is painful but valuable

**If interview context is "evaluating / hasn't decided":**
- Focus on Sections 2 (old way), 3d (first thought), and 4a-4b (push and pull)
- Skip 3a (deciding) — it hasn't happened yet
- Add: "What would need to be true for you to make a change?" and "What's stopping you right now?"

**If existing switch analyses have evidence gaps:**
- Add targeted questions for the weak areas. For example:
  - If habit forces are thin across interviews: add 2 extra habit questions and a bold interviewer note: "⚠️ Habit forces are thin in your existing data. Spend extra time here."
  - If timeline stages are frequently `not_discussed`: add extra probes for those specific stages
  - If `evidence_strength.direct_quotes` is consistently low: add a note about getting verbatim quotes

**If manifest has product/target_user info:**
- Replace generic placeholders ({old solution}, {new solution}, {do the job}) with product-specific language
- Tailor the "Old Way" questions to the target user's role and context

### Red Flags Reference

Always include this section at the end of the script:

```markdown
## Red Flags to Watch For

These patterns indicate you're getting low-quality data. Redirect when you spot them.

| Red Flag | What It Sounds Like | Redirect |
|----------|---------------------|----------|
| **Hypothetical language** | "I would...", "I think I'd..." | "I want to hear what actually happened. Take me back to that moment." |
| **Vague emotions** | "It was frustrating", "I was happy" | "Tell me about a specific time you felt that way. What happened?" |
| **Category answers** | "We needed better analytics" | "What specifically couldn't you do? Walk me through the last time that was a problem." |
| **No dates or people** | "At some point we decided..." | "Was that before or after [event]? Who was in the room?" |
| **Feature lists** | "It has real-time dashboards and API access and..." | "Which of those mattered most to YOU? Why that one?" |
| **Pleasing the interviewer** | "Your product is great because..." | "I appreciate that, but I'm more interested in the messy middle. What almost stopped you?" |
```

### Interview Tips

Always include this section:

```markdown
## Tips for a Great Switch Interview

1. **Record everything.** Use Fireflies, Otter, or your phone. You cannot take notes and listen at the same time.
2. **Shut up.** The best interviewers talk 20% of the time. Ask the question, then wait. Silence is productive.
3. **Follow the energy.** When they lean in or speed up, you've hit something. Probe deeper.
4. **No leading questions.** Not "Was it frustrating?" but "How did that go?" Let them name the emotion.
5. **Get the story, not the opinion.** "What happened?" beats "What do you think about...?" every time.
6. **30-45 minutes is the sweet spot.** Under 20 = too shallow. Over 60 = diminishing returns.
7. **The first answer is never the real answer.** Ask "why?" at least 3 times. The good stuff is 2-3 layers deep.
```

## Human Review

Present the generated script for review using AskUserQuestion:

> **Interview Script Generated**
>
> **Target:** {interviewee context}
> **Sections:** 6 (Opening → Old Way → Timeline → Forces → Reflect → Wrap-up)
> **Estimated duration:** 30-45 minutes
> **Customizations applied:** {list customizations, e.g., "Extra habit probes based on evidence gaps", "Churn-focused framing"}
>
> Options:
> - A) Looks good, save it
> - B) I want to edit something (tell me what to change)
> - C) Start over

If the user chooses B, make the requested changes and re-present.

## Write and Commit

1. Write the markdown file to `.jtbd/interviews/interview-script-{context-slug}-{YYYYMMDD}.md` using the Write tool.

The `context-slug` should describe the interview target:
- If a specific person: `{first-name}-{role-slug}` (e.g., `sarah-ops-manager`)
- If a persona: `{persona-slug}` (e.g., `churned-enterprise-user`)
- If general: `general`

Create the `.jtbd/interviews/` directory if it doesn't exist.

2. If `GIT` is `yes` and the manifest has `auto_commit: true`:

```bash
git add .jtbd/interviews/{filename}.md
git commit -m "jtbd: add interview script for {context description}"
```

If the commit fails, write the file but skip the commit. Tell the user: "File written to .jtbd/interviews/{filename}.md but not committed. Run `git add` and `git commit` manually."

3. If `GIT` is `no`: write the file only.

4. Tell the user what was created and where:

> "Interview script saved to `.jtbd/interviews/{filename}.md`"
>
> **Next steps:**
> - Print it or open it on your phone during the interview
> - Record the interview (Fireflies, Otter, or voice memo)
> - After the interview, run `/jtbd-switch` with the transcript
> - After 3+ switch analyses, run `/jtbd-patterns` to find cross-interview patterns
