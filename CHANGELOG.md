# Changelog

All notable changes to this project will be documented in this file.

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
