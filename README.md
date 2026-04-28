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

```bash
curl -sSL https://raw.githubusercontent.com/philippossavvides/jtbd/main/install.sh | bash
```

Or manually clone it:

```bash
git clone https://github.com/philippossavvides/jtbd.git ~/.claude/skills/jtbd
```

### Try it

Run `/jtbd-switch` in Claude Code using our example transcript:

```
/jtbd-switch examples/sample-transcript.txt
```

Or just paste your own interview text:

```
/jtbd-switch
```

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
| `/jtbd-demo` | Available | 5-minute interactive walkthrough to learn the framework. |
| `/jtbd-switch` | Available | Analyze a single interview transcript into a structured Switch format. |
| `/jtbd-interview` | **Available** | Generate a custom Switch interview script. |
| `/jtbd-patterns` | **Available** | Find patterns across three or more switch analyses. |
| `/jtbd-pipeline` | **Available** | Batch-process a folder of transcripts through the entire pipeline. |
| `/jtbd-forces` | **Available** | Create an HTML forces diagram. |
| `/jtbd-map` | **Available** | Synthesize your patterns into a full job map. |
| `/jtbd-brief` | **Available** | Draft a product brief straight from the .jtbd/ data. |

## The idea

Most product research happens in isolated apps. You do the analysis in one place, write the spec somewhere else, and write code in a completely different environment. Insights get lost in translation.

We built JTBD skills to put research right where the code lives. The `.jtbd/` directory acts as a git-native data layer. You can literally `git blame` a feature to see the exact customer interview that justified building it.

## Works standalone, chains with gstack

You only need Claude Code to run these skills. There are no other dependencies.

If you happen to use [gstack](https://github.com/garrytan/gstack), the skills chain naturally into its workflow:

```
/jtbd-interview → /jtbd-switch → /jtbd-patterns → /jtbd-brief → /office-hours → /plan-eng-review → /ship
```

You can also run the whole batch at once: `/jtbd-pipeline path/to/transcripts/`

## Learn JTBD

If you are new to Jobs to Be Done, try running `/jtbd-demo` for a quick interactive tour. We also wrote a [full methodology guide](docs/methodology.md) you can read.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) to learn how to add skills, improve the extraction prompts, or share example transcripts.

## License

MIT
