# jtbd: Jobs to Be Done Skills for Antigravity, Gemini & Claude Code

Open source skills for turning customer interview transcripts into structured demand evidence versioned in git, based on [Moesta's Switch methodology](docs/methodology.md).

## What it does

Paste an interview transcript into your coding agent (Google Antigravity, Gemini, or Claude Code). The skills extract structured YAML in your repository containing:

- **Switching timeline:** first thought, passive looking, active looking, deciding, and consuming.
- **The four forces:** push, pull, anxiety, and habit, with verbatim quotes and intensity scores (1-10).
- **Job story:** formatted as "When [situation], I want [motivation], so I can [outcome]."
- **Evidence strength score:** grading quote fidelity, behavioral specificity, and timeline clarity.

Output saves to `.jtbd/` so you can commit demand evidence alongside source code and review customer research in pull requests.

## Quick start

### Install

#### In Google Antigravity & Gemini
Clone into your Antigravity plugin configuration:
```bash
git clone https://github.com/savvides/jtbd.git ~/.gemini/config/plugins/jtbd
```
When working inside this repository, Antigravity and Gemini automatically discover `GEMINI.md` and all skills.

#### In Claude Code
Run inside Claude Code:
```
/plugin marketplace add savvides/jtbd
/plugin install jtbd@jtbd
```
Then restart Claude Code or run `/reload-plugins`.

Verify installation by typing `/jtbd` to confirm the eight commands appear.

### Try it

Run the guided walkthrough using bundled sample data:

```
/jtbd-demo
```

Or analyze a transcript with:

```
/jtbd-switch
```

To run with the bundled sample transcript, pass `<plugin-dir>/examples/sample-transcript.txt` as printed by `/jtbd-demo`.

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

The repo also includes `demo/.jtbd/`, a complete sample project with three interviews, pattern clustering, and a job map.

## Available skills

| Skill | Status | Description |
|---|---|---|
| `/jtbd-demo` | Stable | 5-minute interactive walkthrough of the framework. |
| `/jtbd-switch` | Stable | Analyze a single interview transcript into structured Switch YAML. |
| `/jtbd-interview` | Stable | Generate a customized Switch interview script. |
| `/jtbd-patterns` | Stable | Cluster patterns across three or more switch analyses. |
| `/jtbd-pipeline` | Stable | Batch-process a folder of transcripts through switch and pattern analysis. |
| `/jtbd-forces` | Stable | Generate a standalone HTML visual diagram of the four forces. |
| `/jtbd-map` | Stable | Synthesize patterns into a structured Job Map (YAML + Markdown). |
| `/jtbd-brief` | Stable | Draft a product brief from Job Map data. |

## Boundaries

- **Bring your own transcript:** any transcription tool (Fireflies, Otter, Zoom) works.
- **No external servers:** no cloud accounts, no dashboards, no tracking. Output lives in local YAML/Markdown files.
- **Not a CRM:** captures switching dynamics and motivation, not sales pipeline stages.
- **Requires customer conversations:** prompts organize real interviews. Empty input produces no output.
- **Prompt-based:** output follows the defined schema strictly, while prose wording reflects model synthesis.

## Token usage

Skills run against your own agent model:

| Command | Input size | Notes |
|---|---|---|
| `/jtbd-demo` | None | Reads bundled sample data. |
| `/jtbd-switch` | One transcript | Scales with transcript length (typically 5,000-10,000 words). |
| `/jtbd-patterns` | All switch files | Reads all switch analyses into context simultaneously. |
| `/jtbd-pipeline` | Folder of transcripts | For 4+ transcripts, dispatches up to 4 parallel agents followed by pattern synthesis. |

## Rationale

Product research often gets trapped in separate tools, disconnected from the codebase. By storing demand evidence in `.jtbd/`, engineering and product teams can trace features directly back to the customer interviews that justified them.

## Workflow chaining

Skills can be run independently or chained together in sequence:

```
/jtbd-interview → /jtbd-switch → /jtbd-patterns → /jtbd-forces → /jtbd-map → /jtbd-brief
```

Or batch-process transcripts in one step:
```
/jtbd-pipeline path/to/transcripts/
```

If you use [gstack](https://github.com/garrytan/gstack), briefs feed directly into `/office-hours` and `/plan-eng-review`.

## Troubleshooting

**Installed the plugin and commands do not appear:**
Restart your agent session or reload plugins.

**`/plugin marketplace add savvides/jtbd` fails:**
Verify internet access and ensure the repository URL is reachable.

**Validating YAML files:**
Validate any generated `.jtbd/` file with Python:
```bash
python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" .jtbd/switches/your-file.yml
```

## Learn JTBD

Run `/jtbd-demo` for an interactive introduction, or read the [methodology guide](docs/methodology.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on adding skills, refining prompts, or contributing anonymized sample transcripts.

## License

MIT

