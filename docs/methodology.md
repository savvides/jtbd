# The Switch: A Founder's Guide to Jobs to Be Done

This is a practical guide to Bob Moesta's Switch methodology, written for startup founders who want to understand why customers switch products. No academic jargon. Just the parts you need to do better interviews and build the right thing.

## The core idea

People don't buy products. They hire them to make progress in their lives.

That sounds abstract. Here's what it means concretely: your customer had a life before your product. They were getting the job done somehow, even if badly. Something happened that made them start looking for something better. They found options. They picked one. They switched.

That story, the switching story, tells you everything you need to know about what to build.

## The four forces

Every switch is driven by four forces. Two push toward the switch. Two resist it.

```
FORCES DRIVING THE SWITCH          FORCES RESISTING THE SWITCH
========================          ===========================

Push of the current       ──►     ◄──  Anxiety of the new
situation                                solution
"What's broken right now"         "What if it doesn't work?"

Pull of the new           ──►     ◄──  Habit of the present
solution
"What's attracting me"            "What I'm used to"
```

**Push** is what's wrong with the status quo. The reporting tool crashes during month-end. The spreadsheet has formula errors nobody can find. The current vendor missed a deadline.

Push is always a specific event or pattern, not a vague feeling. "It was frustrating" is not push. "It crashed for 3 days during our biggest month" is push.

**Pull** is what attracts the person to the new solution. Real-time dashboards. A single source of truth. A vendor who picks up the phone.

Pull is about the imagined future state, not features. The customer isn't attracted to "real-time sync." They're attracted to "I can see the numbers whenever I want without asking someone."

**Anxiety** is what scares the person about switching. Will the data migration work? Will my team hate the new tool? What if the new vendor is worse?

Anxiety is the silent killer of sales. People don't tell you about their anxieties. You have to probe for them. "What almost stopped you from switching?"

**Habit** is the comfort of the familiar. The team knows the old tool's quirks. There are workarounds for every bug. "It's not great, but we know how it works."

Habit is underestimated. People tolerate enormous pain if the alternative requires change. The switch happens when Push + Pull overwhelms Anxiety + Habit.

## The switching timeline

Every switch follows a timeline. The interview reconstructs it.

```
FIRST        PASSIVE       ACTIVE        DECIDING      CONSUMING
THOUGHT      LOOKING       LOOKING
  │             │             │              │              │
  ▼             ▼             ▼              ▼              ▼
"Something    "Casually     "Actively      "Chose this    "Using the
 is wrong"     noticing      evaluating     specific       new thing"
               options"      options"       solution"
```

**First thought** — The moment the person first considered that things could be different. Always triggered by a specific event. "Our tool went down for 3 days during month-end close."

**Passive looking** — A period of casual awareness. Asking peers. Reading articles. Noticing ads. Not actively searching, just... open to alternatives.

**Active looking** — Something escalated the urgency. They're now signing up for trials, scheduling demos, comparing features. Ask: "What changed between casually noticing and actively searching?"

**Deciding** — They chose a specific solution. The deciding factors often surprise you. It's rarely the feature matrix. It's often something emotional or contextual: "My CEO saw the demo and said yes immediately."

**Consuming** — The actual switch. Onboarding, migration, team adoption. This is where anxiety becomes real. "We had to manually re-enter 3 months of data."

## How to do a Switch interview

The goal is to reconstruct the switching timeline with as much specificity as possible. Start from the end and work backward.

### Opening

"Tell me about the last time you switched from one [product category] to another."

If they haven't switched recently: "Tell me about the last time you seriously considered switching, even if you didn't."

### Timeline reconstruction

Walk backward through the timeline:

1. **Start with the decision:** "What did you end up choosing? When was that?"
2. **Active looking:** "Before you chose that, what other options did you evaluate? How did you find them?"
3. **Passive looking:** "Before you started actively looking, was there a period where you were just aware that alternatives existed?"
4. **First thought:** "Take me back to the very first moment you thought 'maybe I should look for something different.' What happened?"
5. **Consuming:** "After you decided, what was the onboarding like? What was harder than expected?"

### Forces probing

For each force, probe with specific questions:

**Push:** "What was happening with [current solution] that made you start looking?" Follow up: "Can you give me a specific example of when that was really painful?"

**Pull:** "What about [new solution] attracted you?" Follow up: "What did you imagine your life would look like after switching?"

**Anxiety:** "What almost stopped you from switching?" Follow up: "Was there a moment where you thought 'maybe this isn't worth it'?"

**Habit:** "What was comfortable about the old way of doing things?" Follow up: "Was there anything your team missed about the old tool after switching?"

### Red flags to watch for

- **"I would..."** — Hypothetical language means they're speculating, not recalling. Redirect: "Tell me about a time you actually did that."
- **"Everyone needs..."** — Category-level answers. Push for specificity: "Who specifically? Can you name one person?"
- **"It was frustrating"** — Vague emotions. Push for events: "What specifically happened that frustrated you?"
- **No specific dates or events** — Timeline is too abstract. Push: "Was this before or after [reference event]? Roughly how many weeks/months?"

## How the skills use this

Run `/jtbd-interview` to generate a customized interview script based on your product context and any evidence gaps from prior interviews. Then run the interview.

When you run `/jtbd-switch` on an interview transcript, it extracts:

1. The **timeline** (first thought through consuming) with confidence levels
2. The **four forces** (push, pull, anxiety, habit) with verbatim quotes and intensity scores
3. A **job story** in Klement format: "When [situation], I want [motivation], so I can [outcome]"
4. An **evidence strength score** rating the quality of the interview data

The output is a YAML file committed to `.jtbd/switches/` in your repo. After 3+ interviews, patterns will emerge across the switch analyses, revealing the real jobs your product needs to serve.

## Further reading

- Bob Moesta & Greg Engle, "Demand-Side Sales 101" — The practitioner's guide to Switch interviews
- Clayton Christensen, "Competing Against Luck" — The theoretical foundation
- Alan Klement, "When Coffee and Kale Compete" — Job stories and practical application
- Bob Moesta, "Learning to Build" — How to use JTBD for product development
