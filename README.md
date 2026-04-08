# jtbd — Jobs to Be Done Skills for Claude Code

Turn customer interview transcripts into structured, version-controlled demand evidence. Built on [Moesta's Switch methodology](docs/methodology.md).

## What it does

You run a customer interview. You paste the transcript. You get a structured YAML file in your repo that captures:

- **The switching timeline** — first thought, passive looking, active looking, deciding, consuming
- **The four forces** — push, pull, anxiety, habit (each with direct quotes and intensity scores)
- **A job story** — "When [situation], I want [motivation], so I can [outcome]"
- **Evidence strength scoring** — how solid is the data from this interview?

The output lives in a `.jtbd/` directory committed alongside your code. Your demand evidence is now version-controlled, reviewable, and traceable — just like your source code.

## Quick start

### Install

```bash
curl -sSL https://raw.githubusercontent.com/philippossavvides/jtbd/main/install.sh | bash
```

Or manually:

```bash
git clone https://github.com/philippossavvides/jtbd.git ~/.claude/skills/jtbd
```

### Try it

Run `/jtbd-switch` in Claude Code with the included example transcript:

```
/jtbd-switch examples/sample-transcript.txt
```

Or paste your own interview transcript:

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

See `demo/.jtbd/` for a fully-populated example with 3 interviews and pattern analysis.

## Available skills

| Skill | Status | What it does |
|-------|--------|-------------|
| `/jtbd-demo` | Available | 5-minute guided walkthrough of JTBD — learn the framework by seeing it in action |
| `/jtbd-switch` | Available | Analyze one interview transcript into a structured Switch analysis |
| `/jtbd-interview` | **Available** | Generate a customized Switch interview script |
| `/jtbd-patterns` | Coming soon | Find patterns across 3+ switch analyses |
| `/jtbd-forces` | Coming soon | Generate an HTML forces diagram |
| `/jtbd-map` | Coming soon | Synthesize patterns into a job map |
| `/jtbd-brief` | Coming soon | Generate a product brief from .jtbd/ data |

## The idea

Every existing JTBD tool treats research as a standalone activity in a separate app. You analyze in one tool, write specs in another, build in a third. By the time an insight reaches code, it's been diluted.

JTBD skills put the research where the code is. The `.jtbd/` directory is a git-native data layer — demand evidence committed alongside the code it justifies. `git blame` your way from a feature back to the interview that demanded it.

## Works standalone, chains with gstack

JTBD skills require only Claude Code. No other dependencies.

If you also have [gstack](https://github.com/garrytan/gstack) installed, the skills chain naturally into gstack's workflow:

```
/jtbd-interview → /jtbd-switch → /jtbd-patterns → /jtbd-brief → /office-hours → /plan-eng-review → /ship
```

## Learn JTBD

New to Jobs to Be Done? Run `/jtbd-demo` for a 5-minute interactive walkthrough, or read [docs/methodology.md](docs/methodology.md) for the full methodology guide.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new skills, improve extraction quality, or contribute example transcripts.

## License

MIT
