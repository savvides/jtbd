# The Switch: A Founder's Guide to Jobs to Be Done

We wrote this guide to Bob Moesta's Switch methodology for startup founders trying to figure out why customers actually change products. We stripped out the academic theory so you can focus on running better interviews and building the right thing.

## The core idea

People do not just buy products. They hire them to make progress in their lives.

While that might sound a bit abstract, the reality is straightforward. Your customer had a routine before they found your product. They were getting the job done somehow, even if the process was terrible. Eventually, something broke or changed, forcing them to look for a better way. They evaluated a few options, picked one, and made the switch.

Understanding that entire switching story tells you exactly what you need to build.

## The four forces

Every decision to switch is driven by four forces. Two of them push the customer toward making a change, while the other two hold them back.

```text
FORCES DRIVING THE SWITCH          FORCES RESISTING THE SWITCH
========================          ===========================

Push of the current       ──►     ◄──  Anxiety of the new
situation                                solution
"What is broken right now"         "What if it doesn't work?"

Pull of the new           ──►     ◄──  Habit of the present
solution
"What is attracting me"            "What I am used to"
```

**Push** represents what is actively failing in the status quo. Maybe the reporting tool crashes during month-end close. The spreadsheet has formula errors nobody can find. The current vendor missed a critical deadline. Push is always tied to a specific event or pattern, not a vague feeling. Hearing a customer say "it was frustrating" is not a push. Hearing "it crashed for three days during our biggest month" is a push.

**Pull** is the magnetic appeal of the new solution. Real-time dashboards, a single source of truth, or a vendor who actually picks up the phone. Pull is fundamentally about the customer's imagined future state, not specific features. They are not attracted to "real-time sync" as much as the idea that they can see their numbers whenever they want without having to ask someone else.

**Anxiety** covers everything that scares them about switching. They worry the data migration will fail, their team will hate the new tool, or the new vendor will turn out to be worse than the old one. Anxiety is the silent killer of sales. People rarely volunteer their anxieties, so you have to probe for them by asking things like, "What almost stopped you from switching?"

**Habit** is simply the comfort of the familiar. The team already knows the old tool's quirks and they have workarounds for every bug. People will tolerate an enormous amount of pain if the alternative requires them to change their behavior. The switch only happens when the combination of Push and Pull completely overwhelms Anxiety and Habit.

## The switching timeline

Every switch follows a distinct timeline, and the goal of your interview is to reconstruct it.

```text
FIRST        PASSIVE       ACTIVE        DECIDING      CONSUMING
THOUGHT      LOOKING       LOOKING
  │             │             │              │              │
  ▼             ▼             ▼              ▼              ▼
"Something    "Casually     "Actively      "Chose this    "Using the
 is wrong"     noticing      evaluating     specific       new thing"
               options"      options"       solution"
```

**First thought:** The exact moment the person realized things could be different. This is always triggered by a specific event, like a server going down for three days.

**Passive looking:** A period of casual awareness. They might ask peers, read articles, or start noticing ads. They are not actively searching yet, just keeping an open mind about alternatives.

**Active looking:** Something escalated the urgency. Now they are signing up for trials, scheduling demos, and comparing features. You want to ask them what changed to move them from casually noticing to actively searching.

**Deciding:** The moment they chose a specific solution. The deciding factors often surprise founders because it is rarely about the feature matrix. It is usually something emotional or contextual, like a CEO seeing the demo and saying yes immediately.

**Consuming:** The actual process of switching. This covers onboarding, migration, and team adoption. It is also where the anxiety becomes real, especially when they realize they have to manually re-enter three months of data.

## How to do a Switch interview

Your objective is to reconstruct the timeline with as much specificity as possible. The best way to do this is to start at the end and work your way backward.

### Opening

"Tell me about the last time you switched from one [product category] to another."

If they haven't switched recently, adjust it to: "Tell me about the last time you seriously considered switching, even if you ultimately didn't."

### Timeline reconstruction

Walk backward through their experience:

1. **Start with the decision:** "What did you end up choosing? When was that?"
2. **Active looking:** "Before you chose that, what other options did you evaluate? How did you find them?"
3. **Passive looking:** "Before you started actively looking, was there a period where you were just aware that alternatives existed?"
4. **First thought:** "Take me back to the very first moment you thought 'maybe I should look for something different.' What happened?"
5. **Consuming:** "After you decided, what was the onboarding like? What was harder than expected?"

### Forces probing

Dig into each force with targeted questions:

**Push:** "What was happening with your old setup that made you start looking?" Follow up by asking for a specific example of when it was really painful.

**Pull:** "What about the new product attracted you?" Follow up by asking what they imagined their life would look like after making the switch.

**Anxiety:** "What almost stopped you from switching?" Follow up to find out if there was a moment they thought it might not be worth the effort.

**Habit:** "What was comfortable about the old way of doing things?" Follow up to see if their team missed anything about the old tool.

### Red flags to watch for

- **"I would..."** — Hypothetical language usually means they are speculating instead of recalling an actual event. Redirect them by asking about a time they actually did that.
- **"Everyone needs..."** — Broad category-level answers. Push for specificity by asking them to name one specific person.
- **"It was frustrating"** — Vague emotional statements. Ask them what specifically happened that frustrated them.
- **No specific dates or events** — If the timeline feels too abstract, try anchoring it. Ask if this happened before or after a reference event, or roughly how many weeks ago it was.

## How the skills use this

You can run `/jtbd-interview` to generate a customized interview script based on your product context and any evidence gaps from your previous interviews. 

When you run `/jtbd-switch` on an interview transcript, it extracts:

1. The **timeline** (from first thought through consuming) along with confidence levels.
2. The **four forces** (push, pull, anxiety, habit) complete with verbatim quotes and intensity scores.
3. A **job story** in Klement format: "When [situation], I want [motivation], so I can [outcome]."
4. An **evidence strength score** that rates the quality of the interview data.

This output gets saved as a YAML file in `.jtbd/switches/` inside your repository. Once you have analyzed three or more interviews, patterns start to emerge, showing you the real jobs your product needs to serve.

## Further reading

- Bob Moesta & Greg Engle, "Demand-Side Sales 101" — The practitioner's guide to running Switch interviews.
- Clayton Christensen, "Competing Against Luck" — The theoretical foundation of the framework.
- Alan Klement, "When Coffee and Kale Compete" — A deeper look at job stories and practical applications.
- Bob Moesta, "Learning to Build" — How to use JTBD for actual product development.
