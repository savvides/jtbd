# GitHub Repository Metadata & Release History Design

**Date:** 2026-08-31  
**Status:** Approved  
**Scope:** Repository About metadata configuration and milestone GitHub Releases publication  

---

## 1. Overview

This document specifies the synchronization of GitHub repository metadata ("About" description, homepage, topics) and the creation of GitHub Releases and Git tags for current and key historical releases documented in `CHANGELOG.md`.

---

## 2. GitHub Repository About Configuration

Using `gh repo edit savvides/jtbd`, the repository metadata will be set to:

### 2.1 Description
```text
Jobs to Be Done skills for Google Antigravity, Gemini, and Claude Code. Turn customer interview transcripts into structured, version-controlled demand evidence.
```

### 2.2 Homepage URL
```text
https://github.com/savvides/jtbd
```

### 2.3 Topics
```text
antigravity, gemini, claude-code, claude-code-skills, agent-skills, ai-agents, customer-discovery, jobs-to-be-done, jtbd, startup-tools
```

---

## 3. GitHub Releases & Git Tag Mappings

Releases will be published using `gh release create <tag> --target <commit-hash> --title <title> --notes <notes-markdown>`.

### 3.1 `v1.9.0.0` (Latest Release)
- **Target Commit:** `eec9ca7` (or current `main` HEAD)
- **Tag:** `v1.9.0.0`
- **Title:** `v1.9.0.0 — Formal Schema Specifications & Provenance Tracking`
- **Release Notes:**
  ```markdown
  ### Added
  - **Formal Schema Specifications (`docs/schema/`):**
    - Added JSON/YAML schema definitions for all `.jtbd/` artifacts: `manifest.schema.yml`, `switch.schema.yml`, `patterns.schema.yml`, and `job-map.schema.yml`.
    - Added `docs/schema/README.md` defining data contracts, field definitions, and design goals.
  - **Traceable Provenance Metadata:**
    - Added top-level `provenance` block (`skill`, `version`, `created_at`) across all generated YAML artifacts and skill templates (`/jtbd-switch`, `/jtbd-patterns`, `/jtbd-map`).

  ### Changed
  - **Unified Schema Versioning:**
    - Standardized on `schema_version: 1` across all switch analyses and job maps in addition to manifests and patterns.
  - **Validator Enhancements:**
    - `scripts/validate.py` now enforces strict schema versioning (`schema_version: 1`), top-level key contracts, and `provenance` metadata across all `.jtbd/` YAML files with expanded self-test coverage.
  ```

### 3.2 `v1.8.0.0`
- **Target Commit:** `1645577`
- **Tag:** `v1.8.0.0`
- **Title:** `v1.8.0.0 — Stable Multi-Agent Skills & Voice Polish`
- **Release Notes:**
  ```markdown
  ### Changed
  - **All 8 skills marked Stable:**
    - `/jtbd-map`: Updated schema to emit full YAML representation (`job`, `frequency`, `confidence`, `steps`, `switching_trigger`, `forces_summary`) matching demo data and providing complete input for product briefs.
    - `/jtbd-brief`: Standardized input processing to consume the unified Job Map schema directly.
    - `/jtbd-forces`: Added explicit layout, typography, CSS Grid, intensity badges, and inferred quote styling rules to ensure reproducible, accessible standalone HTML output.
    - Removed Preview labels and limitations across all documentation.

  ### Improved
  - **Voice and Documentation Quality:**
    - Audited all repository documentation, prompts, guides, and installer scripts with the `avoid-ai-writing` rubric to remove AI writing tells, hollow intensifiers, and formulaic constructions.
    - Clear multi-agent positioning across Google Antigravity, Gemini, and Claude Code throughout all documentation.
  ```

### 3.3 `v1.7.0.0`
- **Target Commit:** `f5b2af7`
- **Tag:** `v1.7.0.0`
- **Title:** `v1.7.0.0 — Google Antigravity & Gemini Support`
- **Release Notes:**
  ```markdown
  ### Added
  - **First-class support for Google Antigravity and Gemini.** jtbd is now dual-compatible with Google Antigravity, Gemini, and Claude Code from a single source of truth:
    - Added `GEMINI.md` (and `AGENTS.md`) at the repository root, providing Antigravity and Gemini with project instructions, skill listings, schema definitions, and skill routing rules.
    - Added Antigravity plugin manifest and layout under `plugins/jtbd/plugin.json` and `plugins/jtbd/skills/`.
    - Skill preambles in `/jtbd-demo` and `/jtbd-pipeline` now probe Antigravity plugin paths (`~/.gemini/config/plugins/jtbd`), Claude plugin paths (`${CLAUDE_PLUGIN_ROOT}`), workspace root, and global skill paths.
    - `validate.py` now validates `GEMINI.md` skill listings alongside `CLAUDE.md` and `README.md`, and validates that skill preambles probe Antigravity plugin paths in addition to Claude plugin roots.
  ```

### 3.4 `v1.6.0.1`
- **Target Commit:** `de77c45`
- **Tag:** `v1.6.0.1`
- **Title:** `v1.6.0.1 — Plugin Asset Path & Preamble Fixes`
- **Release Notes:**
  ```markdown
  ### Fixed
  - Fixed `/jtbd-demo` asset resolution under Claude Code plugin installs by probing `${CLAUDE_PLUGIN_ROOT}`.
  - Declared `Bash` in `allowed-tools` for `/jtbd-demo` so preamble scripts execute.
  - Anchored `/jtbd-pipeline` extraction rules to resolved plugin root.
  ```

### 3.5 `v1.6.0.0`
- **Target Commit:** `b12e04b`
- **Tag:** `v1.6.0.0`
- **Title:** `v1.6.0.0 — Claude Code Plugin Conversion`
- **Release Notes:**
  ```markdown
  ### Added
  - Migrated repository to a first-class Claude Code plugin using `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
  ```

### 3.6 `v1.5.0.0`
- **Target Commit:** `e400f2f`
- **Tag:** `v1.5.0.0`
- **Title:** `v1.5.0.0 — Origin Repository Repointing & Structural Validator`
- **Release Notes:**
  ```markdown
  ### Changed
  - Repointed documentation and installer to public origin `savvides/jtbd`.
  - Added `scripts/validate.py` structural validator and GitHub Actions CI workflow.
  ```

---

## 4. Verification & Success Criteria

1. `gh repo view` displays the updated description, homepage, and topics.
2. `git tag -l` and `gh release list` display all published release tags.
3. `gh release view v1.9.0.0` shows the correct title, tag, target commit, and release notes.
