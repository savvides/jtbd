# Changelog

All notable changes to this project will be documented in this file.

## [1.6.0.1] - 2026-08-30

### Fixed
- **`/jtbd-demo` dead-ended for everyone who installed the plugin.** Its preamble looked for the example transcript and demo data in the jtbd repo root or in `~/.claude/skills/jtbd/`. A plugin install lands under `~/.claude/plugins/`, so a user following the README — install the plugin, run `/jtbd-demo` — got "Demo files not found" and stopped. Both `/jtbd-demo` and `/jtbd-pipeline` now check `${CLAUDE_PLUGIN_ROOT}` first and fall back to the repo root, so the demo works from any directory.
- The message `/jtbd-demo` printed when it could not find its files told you to `git clone` the repo into `~/.claude/skills/jtbd`. That is the install v1.6.0.0 removed for registering nothing, so the recovery advice rebuilt the broken state. It now names the two plugin commands and points at the issue tracker.

### For contributors
- `CLAUDE.md` marks `/jtbd-forces`, `/jtbd-map` and `/jtbd-brief` as Preview, matching README. `TESTING.md` documents the `claude plugin validate` CI steps, records why the CI job has to stay named `run-lint`, and lists the six plugin-manifest fixtures added in 1.6.0.0.

## [1.6.0.0] - 2026-08-30

### Fixed
- **Every documented install path produced skills Claude Code could not see.** `install.sh` cloned this repo to `~/.claude/skills/jtbd/`, which puts every `SKILL.md` two levels below `~/.claude/skills/`. Claude Code discovers personal skills exactly one level deep, so the install landed eight files and registered nothing. Verified against a sandboxed `HOME`: all eight `SKILL.md` files present, none at a discovery path, and no `~/.claude/commands/` created. jtbd is now a Claude Code plugin — `/plugin marketplace add savvides/jtbd`, then `/plugin install jtbd@jtbd`.
- **Command wrappers only worked from one directory.** All eight `.claude/commands/*.md` files pointed at a bare relative path (`jtbd-switch/SKILL.md`), which resolves only when the shell's cwd is this repo's root — exactly the case the README says is not the use case. They now anchor with `${CLAUDE_PROJECT_DIR}`, and the validator rejects the bare form outright.
- `install.sh` no longer performs an install that cannot work. It prints the two plugin commands and explains why cloning into `~/.claude/skills/` does not register anything.

### Added
- `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`. The repository is its own plugin marketplace, so installs are versioned and `/plugin update` and uninstall work.
- `validate.py` checks the plugin manifest: that it exists, is valid JSON, that `skills` is a list of `./`-relative paths, that every entry resolves to a real `SKILL.md`, and that no skill on disk is missing from the list. Each way the manifest can silently drop a command has its own self-test fixture; disabling the check body fails all six.
- CI runs `claude plugin validate` against both manifests. That is the authoritative check, maintained against the real plugin loader; the validator's own checks mirror the path resolution so contributors without the CLI catch the common mistake locally.
- README sections for what jtbd is *not*, what it costs to run (including that `/jtbd-pipeline` fans out to 4 concurrent agents), and troubleshooting a plugin install that registers no commands.

### Changed
- The CI job is renamed `validate` -> `run-lint`, because the "Protect Main Branch" ruleset requires a status check named `run-lint` and no workflow produced one. The required check could never report, so every pull request to `main` was permanently unmergeable through the normal path. The job id is what GitHub uses as the check context, so it has to match the rule.
- Skill frontmatter no longer carries `version`. It is not a Claude Code frontmatter field and not one of the six Agent Skills spec fields, so carrying it blocked claude.ai packaging — and all eight were stale at `1.0.0` against a `VERSION` of `1.5.0.1`. The plugin manifest is now the single source of truth for the collection's version.
- `/jtbd-forces`, `/jtbd-map` and `/jtbd-brief` are marked **Preview** in the README rather than Available, with the reason stated: `/jtbd-map` emits a schema that does not carry every field `/jtbd-brief` requires, so on the default path part of a generated brief has no source in your data. Tracked in TODOS.md.

## [1.5.0.1] - 2026-08-30

### Fixed
- `/jtbd-pipeline` reported success without committing anything when it ran on fewer than 3 transcripts. Pattern analysis is skipped at that size, so `.jtbd/patterns/` never exists, and the unmatched glob in `git add` aborted the whole command — leaving every switch analysis untracked while the summary said the run was complete. It now stages directories instead of globs, and says so plainly when there is nothing to commit.

## [1.5.0.0] - 2026-08-29

### Added
- `python3 scripts/validate.py` checks the repo's structure before you commit: skill frontmatter, command wrappers, YAML example data, and availability claims. `--self-test` replays twelve fixtures pinning the regressions these checks were written to catch. Run it before opening a PR.
- CI runs the self-test and the validator on every push to `main` and every pull request, so a broken skill definition is caught before review.
- `TESTING.md` describing every check, the escapes available, and how to add a new one.
- `/jtbd-forces`, `/jtbd-map` and `/jtbd-brief` now end by telling you what to run next, like the older skills do.

### Fixed
- `/jtbd-map` would not load: a stray comment sat above its frontmatter, and the same comment displaced its description in the slash-command picker.
- Following the next steps printed by `/jtbd-patterns`, `/jtbd-pipeline` or `/jtbd-demo` sent you to `/jtbd-brief`, which exits immediately without a job map. `/jtbd-map` is now named in each chain, and in the README workflow, which dead-ended the same way.
- `/jtbd-map` and `/jtbd-brief` told you to run the wrong command when their input directory was missing, naming `.jtbd/` instead of the directory they actually need.
- `/jtbd-forces` described each force as a single quote plus intensity. Forces are lists, and a quote is empty when the force was inferred rather than stated.
- Skills that ship were still advertised as unavailable in three places.
- `CONTRIBUTING.md` said every `.jtbd/` file carries `schema_version: 1`, and `CLAUDE.md` attributed it to switch analyses. Neither switch analyses nor job maps carry it.

### Changed
- `CONTRIBUTING.md` now states that a skill needs a paired `.claude/commands/` wrapper and points at the validator to run before opening a PR.
- The pull request test plan now asks you to run the validator, instead of a one-off `yaml.safe_load` snippet against a single file you name by hand.

## [1.4.0.0] - 2026-04-27

### Added
- `/jtbd-forces` skill: generates an HTML diagram of the four forces driving a switch.
- `/jtbd-map` skill: synthesizes patterns into a structured Job Map (YAML + Markdown).
- `/jtbd-brief` skill: drafts a JTBD-native product brief straight from the .jtbd/ data.

### Fixed
- Improved preamble checks in all new skills to provide clearer error messages when directories are missing.

## [1.3.0.1] - 2026-04-27

### Added
- Added Claude command configs for `jtbd-demo` and `jtbd-switch` for editorial reviews
- Added base `.jtbd/manifest.yml` and `.gitignore` setup for demand evidence tracking

## [1.3.0] - 2026-04-24

### Added
- `/jtbd-pipeline` skill: batch-process multiple interview transcripts through the full analysis pipeline. Accepts a directory of transcript files or Fireflies meeting IDs. Runs switch analysis on each transcript (parallel when 4+), then cross-interview pattern analysis. One command to go from raw transcripts to structured demand evidence

## [1.2.0] - 2026-04-24

### Added
- `/jtbd-patterns` skill: find cross-interview patterns across 3+ switch analyses. Clusters recurring jobs, identifies force patterns and timeline patterns, surfaces evidence gaps, and generates actionable recommendations for positioning, onboarding, and next interviews

## [1.1.0] - 2026-04-08

### Added
- `/jtbd-interview` skill: generate a customized Switch interview script tailored to your product, target user, and gaps in your existing evidence. Supports four interview contexts (switched-to, churned, competitor, evaluating) with Moesta's backward-timeline technique and force-probing questions

## [1.0.0] - 2026-04-08

### Added
- `/jtbd-switch` skill: analyze a customer interview transcript into a structured Switch analysis (YAML)
- `/jtbd-demo` skill: 5-minute guided walkthrough of the JTBD framework using sample data
- `.jtbd/` directory structure: git-native demand evidence (manifest, switches, patterns, jobs)
- `docs/methodology.md`: founder-friendly guide to Moesta's Switch framework
- `examples/`: sample interview transcript with expected output for immediate testing
- `demo/.jtbd/`: fully-populated sample project with 3 interviews, patterns, and job map
- `install.sh`: one-line installer with supply chain safeguards (pinned tags, preview before action)
- GitHub issue templates (new skill request, bug report, methodology question) and PR template
- `CONTRIBUTING.md`: guide for adding new skills and contributing example transcripts
