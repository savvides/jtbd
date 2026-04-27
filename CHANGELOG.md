# Changelog

All notable changes to this project will be documented in this file.

## [1.4.0.0] - 2026-04-27

### Added
- `/jtbd-forces` skill: generates an HTML diagram of the four forces driving a switch.
- `/jtbd-map` skill: synthesizes patterns into a structured Job Map (YAML + Markdown).
- `/jtbd-brief` skill: drafts a JTBD-native product brief straight from the .jtbd/ data.

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
