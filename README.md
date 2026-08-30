# jtbd: Jobs to Be Done Skills for Claude Code

These tools convert raw customer interviews into structured demand evidence you can actually version control. They are based on [Moesta's Switch methodology](docs/methodology.md).

## What it does

After running a customer interview, you paste the transcript into Claude Code. The skills generate a YAML file in your repository containing:

- **The switching timeline:** first thought, passive looking, active looking, deciding, and consuming.
- **The four forces:** push, pull, anxiety, and habit, complete with direct quotes and intensity scores.
- **A job story:** formatted as "When [situation], I want [motivation], so I can [outcome]."
- **Evidence strength scoring:** an assessment of how reliable the interview data actually is.

This output gets saved to a `.jtbd/` directory so you can commit it alongside your project. Your demand evidence becomes reviewable and traceable in the exact same way you manage source code.

## Quick start

### Install

Run these two commands inside Claude Code:

```
/plugin marketplace add savvides/jtbd
/plugin install jtbd@jtbd
```

Then restart Claude Code, or run `/reload-plugins`.

Verify it worked by typing `/jtbd` and checking that eight commands appear. If none do, see [Troubleshooting](#troubleshooting).

### Try it

Run the guided walkthrough, which needs no setup and no transcript of your own:

```
/jtbd-demo
```

Or analyze the example transcript that ships with the plugin:

```
/jtbd-switch
```

and paste in `examples/sample-transcript.txt`, or any interview text of your own.

### What you get

```
your-repo/
├── src/
├── .jtbd/
│   ├── manifest.yml
│   ├── switches/
│   │   └── sarah-ops-manager-20260407.yml   <-- structured demand evidence
│   └── raw/                                  <-- gitignored transcripts
└── ...
```

Check out `demo/.jtbd/` to see a fully populated project with three interviews and pattern analysis.

## Available skills

| Skill | Status | What it does |
|-------|--------|-------------|
| `/jtbd-demo` | Stable | 5-minute interactive walkthrough to learn the framework. |
| `/jtbd-switch` | Stable | Analyze a single interview transcript into a structured Switch format. |
| `/jtbd-interview` | Stable | Generate a custom Switch interview script. |
| `/jtbd-patterns` | Stable | Find patterns across three or more switch analyses. |
| `/jtbd-pipeline` | Stable | Batch-process a folder of transcripts through the entire pipeline. |
| `/jtbd-forces` | Preview | Create an HTML forces diagram. Layout is under-specified, so output varies between runs. |
| `/jtbd-map` | Preview | Synthesize your patterns into a full job map. |
| `/jtbd-brief` | Preview | Draft a product brief straight from the `.jtbd/` data. |

**What "Preview" means here.** The three preview skills work, but `/jtbd-map` emits a schema that does not carry every field `/jtbd-brief` asks for, so on the default path part of a generated brief has no source in your data. Tracked in [TODOS.md](TODOS.md); fixing it is the next thing on the list. Use them, read the output critically, and do not treat a brief as finished analysis.

## What this is not

- **Not a transcription service.** Bring your own transcript. Any recorder that produces text works.
- **Not a survey or research platform.** There is no dashboard, no hosting, no accounts. Output is YAML in your repo.
- **Not a CRM.** It records why people switched, not who they are or what they bought.
- **Not a replacement for talking to customers.** It structures interviews you actually ran. Give it nothing and it produces nothing.
- **Not deterministic.** These are prompts. Two runs over the same transcript will differ in wording. The structure is stable; the prose is not.

## What it costs to run

These skills run on your own Claude Code usage. Rough shape, so there are no surprises:

| Command | Typical input | Notes |
|---|---|---|
| `/jtbd-demo` | none | Smallest. Reads bundled example data. |
| `/jtbd-switch` | one transcript | Scales with transcript length. A 60-minute interview is a large input. |
| `/jtbd-patterns` | every switch file | Loads all of them into one context at once. |
| `/jtbd-pipeline` | a folder | **Largest by far.** With 4 or more transcripts it fans out to 4 concurrent agents. Twenty transcripts is twenty analyses plus a pattern pass. |

If you are batch-processing a large folder, start with three or four transcripts to see the shape of the output before running the whole set.

## The idea

Most product research happens in isolated apps. You do the analysis in one place, write the spec somewhere else, and write code in a completely different environment. Insights get lost in translation.

We built JTBD skills to put research right where the code lives. The `.jtbd/` directory acts as a git-native data layer. You can literally `git blame` a feature to see the exact customer interview that justified building it.

## Works standalone, chains with gstack

You only need Claude Code to run these skills. There are no other dependencies.

If you happen to use [gstack](https://github.com/garrytan/gstack), the skills chain naturally into its workflow:

```
/jtbd-interview → /jtbd-switch → /jtbd-patterns → /jtbd-forces → /jtbd-map → /jtbd-brief → /office-hours → /plan-eng-review → /ship
```

You can also run the whole batch at once: `/jtbd-pipeline path/to/transcripts/`

## Troubleshooting

**I installed the plugin and no `/jtbd-*` commands appear.**
Restart Claude Code, or run `/reload-plugins`. Plugin skills load at startup.

**`/plugin marketplace add savvides/jtbd` fails.**
Check the name is exactly `savvides/jtbd`. The marketplace is served from this repository, so it needs network access to GitHub.

**I cloned the repo into `~/.claude/skills/` and nothing works.**
That does not register the skills. Claude Code discovers personal skills at `~/.claude/skills/<skill-name>/SKILL.md`, one level deep, and a clone of this repo puts them two levels deep. Use the plugin install above.

**A generated YAML file will not parse.**
`/jtbd-switch` and `/jtbd-patterns` check their own output before saving. The other skills do not yet. Run `python3 scripts/validate.py` from this repo against your data, or open an issue with the file.

## Learn JTBD

If you are new to Jobs to Be Done, try running `/jtbd-demo` for a quick interactive tour. We also wrote a [full methodology guide](docs/methodology.md) you can read.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) to learn how to add skills, improve the extraction prompts, or share example transcripts.

## License

MIT
