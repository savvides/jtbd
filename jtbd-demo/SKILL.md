---
name: jtbd-demo
version: 1.0.0
description: |
  Guided walkthrough of the JTBD skills. Takes a new user from "what is this?"
  to "I understand the four forces and know what to do next" in about 5 minutes.
  Uses existing example data, no real interview required.
  Use when: "demo", "tutorial", "how does this work", "show me", "getting started".
allowed-tools:
  - Read
  - Glob
  - AskUserQuestion
---

## Preamble

```bash
# Find the jtbd skills root directory
_JTBD_SKILLS=""
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
[ -n "$_ROOT" ] && [ -d "$_ROOT/jtbd-switch" ] && _JTBD_SKILLS="$_ROOT"
[ -z "$_JTBD_SKILLS" ] && [ -d "$HOME/.claude/skills/jtbd/jtbd-switch" ] && _JTBD_SKILLS="$HOME/.claude/skills/jtbd"
echo "JTBD_SKILLS: ${_JTBD_SKILLS:-NOT_FOUND}"

# Verify demo assets exist
_DEMO_OK="yes"
[ -z "$_JTBD_SKILLS" ] && _DEMO_OK="no"
[ "$_DEMO_OK" = "yes" ] && [ ! -f "$_JTBD_SKILLS/examples/sample-transcript.txt" ] && _DEMO_OK="no"
[ "$_DEMO_OK" = "yes" ] && [ ! -f "$_JTBD_SKILLS/examples/expected-output.yml" ] && _DEMO_OK="no"
[ "$_DEMO_OK" = "yes" ] && [ ! -f "$_JTBD_SKILLS/demo/.jtbd/patterns/patterns-20260415.yml" ] && _DEMO_OK="no"
echo "DEMO_ASSETS: $_DEMO_OK"
```

If `DEMO_ASSETS` is `no`: tell the user "Demo files not found. Make sure jtbd is installed correctly. Try: `git clone https://github.com/philippossavvides/jtbd.git ~/.claude/skills/jtbd`" and stop.

## The Demo

You are giving a guided tour of the JTBD skills. Your tone: a friend who just discovered something cool and wants to show you. Not a teacher. Not a salesperson. Just... "look at this, it's neat."

Keep your explanations short. Let the data speak. The sample interview and its analysis are more persuasive than any explanation you could write.

Between each step, use AskUserQuestion with a simple "Ready to continue?" pacing prompt. Do not ask comprehension questions or quiz the user. They'll get it by seeing it.

### Step 1: What is JTBD?

Say this (adapt naturally, don't read it verbatim):

People don't buy products. They hire them to make progress in their lives.

Jobs to Be Done is a framework for understanding WHY customers switch from one solution to another. Not what features they want. Not what they say in surveys. The actual story of what happened, what pushed them away from the old thing, and what pulled them toward the new thing.

These skills turn that story into structured data you can commit alongside your code.

Let me show you what that looks like.

Use AskUserQuestion: "Ready to see a real example?"
Options: A) Let's go  B) Tell me more about JTBD first

If B: Read `$_JTBD_SKILLS/docs/methodology.md` and give a 2-paragraph summary of the four forces and the switching timeline. Then continue to Step 2.

### Step 2: Meet Sarah

Read `$_JTBD_SKILLS/examples/sample-transcript.txt` (the full file, but only SHOW the user key excerpts).

Present these excerpts to the user:

> Here's Sarah, an Operations Manager at a 50-person logistics company. She recently switched reporting tools. Here are the moments that matter from her interview:
>
> **The breaking point:**
> *"Last October, during our month-end close. It went down for three days. I literally couldn't tell my CEO what our numbers were."*
>
> **What she was looking for:**
> *"I wanted my CEO to be able to see the numbers himself, without going through me."*
>
> **What almost stopped her:**
> *"What if we lose three years of data in the switch? That kept me up at night."*
>
> **What kept her on the old tool:**
> *"Everyone had their own way of dealing with DataTracker's quirks."*
>
> Those four quotes map to the four forces in JTBD. Let me show you.

Use AskUserQuestion: "Ready to see the four forces?"
Options: A) Show me  B) Can I read the full transcript first?

If B: Tell the user the transcript is at `examples/sample-transcript.txt` — they can read it with `/read examples/sample-transcript.txt`. Then continue to Step 3.

### Step 3: The Four Forces

Read `$_JTBD_SKILLS/examples/expected-output.yml` and present the forces section.

Show the user:

> When you run `/jtbd-switch` on Sarah's interview, it extracts the **four forces** that drove her switch:
>
> **Push** (what's wrong with the status quo) — intensity: 9/10
> *"I literally couldn't tell my CEO what our numbers were"*
> The old tool failed at the worst possible moment. This is what made her start looking.
>
> **Pull** (what attracts her to the new solution) — intensity: 8/10
> *"I wanted my CEO to be able to see the numbers himself"*
> Not "better charts." Not "faster reports." She wanted to stop being the bottleneck.
>
> **Anxiety** (fear of switching) — intensity: 7/10
> *"What if we lose three years of data in the switch?"*
> This almost killed the deal. She made IT do a test import before signing anything.
>
> **Habit** (comfort with the familiar) — intensity: 5/10
> *"Everyone had their own way of dealing with DataTracker's quirks"*
> The team had built workarounds. Switching meant unlearning those workarounds.
>
> The switch happens when **Push + Pull > Anxiety + Habit**. In Sarah's case: 9 + 8 = 17 vs 7 + 5 = 12. The forces favored switching.
>
> Every quote comes directly from the transcript. Nothing fabricated. The `confidence` field on each force tells you whether it's a direct quote (high), paraphrased (medium), or inferred (low).

Use AskUserQuestion: "Ready to see the timeline?"
Options: A) Next  B) Tell me more about how forces are scored

If B: Explain the evidence strength rubric briefly (1-10 scale, directional not precise, 3 vs 8 is meaningful, 6 vs 7 is noise). Then continue.

### Step 4: The Timeline

Show the timeline from the expected output:

> Every switch follows a timeline. Here's Sarah's:
>
> **First thought** (October 2025) — DataTracker crashes for 3 days during month-end.
> *"That was the moment I thought, okay, something has to change."*
>
> **Passive looking** (~2 months) — Asked peers in Slack communities. Read comparison articles. Just absorbing information.
>
> **Active looking** (~3 weeks) — CEO asked for a recommendation. Now she had a deadline. Signed up for 4 trials, did 2 demo calls.
>
> **Deciding** — CEO sat in on a demo call and said "buy it" before it was over.
>
> **Consuming** (~2 weeks) — Mostly smooth, except manually re-entering 3 months of data.
>
> Notice the trigger between passive and active: her CEO gave her a deadline. That's the moment urgency went from "someday" to "by January." If you're selling to people like Sarah, that trigger is where your timing matters.

Use AskUserQuestion: "Ready to see the job story?"
Options: A) Next

### Step 5: The Job Story

Show the job story:

> From the forces and timeline, the skill generates a **job story**:
>
> *"When my reporting tool fails during month-end close and I can't give leadership the numbers they need, I want a reliable real-time dashboard that leadership can access directly, so I can maintain credibility and stop being the bottleneck between data and decisions."*
>
> The format is: **When** [situation], **I want** [motivation], **so I can** [expected outcome].
>
> This one sentence captures what Sarah is actually hiring the product to do. Not "reporting tool." Not "analytics dashboard." She's hiring it to protect her credibility and give her CEO independence.
>
> If you're building a product for people like Sarah, this job story tells you what to optimize for. It's not about features. It's about the job.

Use AskUserQuestion: "Ready to see what happens after multiple interviews?"
Options: A) Show me patterns

### Step 6: What 3 Interviews Looks Like

Read `$_JTBD_SKILLS/demo/.jtbd/patterns/patterns-20260415.yml` and present the key findings.

> After 3+ interviews, you run `/jtbd-patterns` (coming soon) and it finds what repeats:
>
> **The job that emerged (3/3 interviews):**
> "Get reliable numbers to leadership without being the bottleneck"
>
> **The pattern across all three:**
> - Same push: tools fail or produce conflicting data at critical moments
> - Same pull: self-serve, real-time dashboards that leadership trusts
> - Same anxiety: data migration risk
>
> **What the patterns revealed that no single interview could:**
> - Habit forces were thin — only 2/3 interviews probed the "comfort with old tool" angle deeply enough. That's an evidence gap worth closing.
> - No interviews with end-users (people viewing dashboards). Only buyers. That's a blind spot.
>
> This is where JTBD gets powerful. One interview gives you a story. Three interviews give you a pattern. The pattern tells you what to build.

Use AskUserQuestion: "Ready to try it yourself?"
Options: A) Let's do it  B) I'll come back later

### Step 7: Your Turn

**If A (Let's do it):**

> Run this in Claude Code:
>
> ```
> /jtbd-switch examples/sample-transcript.txt
> ```
>
> That will analyze the same Sarah transcript you just saw, and create a `.jtbd/switches/` file in your repo. You'll get to review the output before it's committed.
>
> After that, do a real interview with one of your customers or users. Record it (Fireflies, Otter, Zoom transcription, whatever). Then run `/jtbd-switch` on that transcript. That's when it gets real.
>
> **The full workflow:**
> 1. `/jtbd-demo` — You just did this. Understand the framework.
> 2. `/jtbd-switch` — Analyze one interview at a time.
> 3. `/jtbd-patterns` — After 3+ interviews, find what repeats. (Coming soon)
> 4. `/jtbd-forces` — Visualize the forces as an HTML diagram. (Coming soon)
> 5. `/jtbd-brief` — Generate a product brief from your research. (Coming soon)
>
> Start with step 2. One real interview. That's the assignment.

**If B (Come back later):**

> No rush. When you're ready:
>
> - Run `/jtbd-switch examples/sample-transcript.txt` to try it with sample data
> - Run `/jtbd-switch` with no arguments to paste your own interview transcript
> - Read `docs/methodology.md` for the full methodology guide
> - Browse `demo/.jtbd/` to see what a complete research project looks like
>
> The best way to learn JTBD is to do one real interview. Everything clicks after that.
