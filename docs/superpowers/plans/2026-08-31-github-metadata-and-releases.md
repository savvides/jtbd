# GitHub Repository Metadata & Release History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update GitHub repository About metadata (description, homepage, topics) and publish current and historical milestone GitHub Releases and Git tags.

**Architecture:** Use GitHub CLI (`gh repo edit`, `gh release create`) and `git` to update remote metadata and publish annotated tags and releases matching `CHANGELOG.md`.

**Tech Stack:** GitHub CLI (`gh`), Git

**Spec:** `docs/superpowers/specs/2026-08-31-github-metadata-and-releases-design.md`

## Global Constraints

- Description: `"Jobs to Be Done skills for Google Antigravity, Gemini, and Claude Code. Turn customer interview transcripts into structured, version-controlled demand evidence."`
- Homepage: `https://github.com/savvides/jtbd`
- Topics: `antigravity, gemini, claude-code, claude-code-skills, agent-skills, ai-agents, customer-discovery, jobs-to-be-done, jtbd, startup-tools`
- All releases must match exact historical merge commits from git history.

---

### Task 1: Update GitHub Repository About Metadata

**Files:**
- N/A (GitHub API / Remote configuration)

**Interfaces:**
- Consumes: Spec section 2 metadata
- Produces: Updated repo description, homepage, topics

- [ ] **Step 1: Update description and homepage via GitHub CLI**

Run:
```bash
gh repo edit savvides/jtbd \
  --description "Jobs to Be Done skills for Google Antigravity, Gemini, and Claude Code. Turn customer interview transcripts into structured, version-controlled demand evidence." \
  --homepage "https://github.com/savvides/jtbd"
```

- [ ] **Step 2: Add multi-agent repository topics**

Run:
```bash
gh repo edit savvides/jtbd --add-topic antigravity --add-topic gemini --add-topic agent-skills --add-topic ai-agents
```

- [ ] **Step 3: Verify repository metadata**

Run:
```bash
gh repo view --json description,homepageUrl,repositoryTopics
```
Expected output shows updated description, homepage, and complete list of topics including `antigravity` and `gemini`.

---

### Task 2: Create Historical Milestone Releases and Git Tags

**Files:**
- N/A (Git tags & GitHub Releases)

**Interfaces:**
- Consumes: Target commit SHAs (`e400f2f`, `b12e04b`, `de77c45`, `f5b2af7`, `1645577`)
- Produces: Published GitHub Releases for `v1.5.0.0`, `v1.6.0.0`, `v1.6.0.1`, `v1.7.0.0`, `v1.8.0.0`

- [ ] **Step 1: Create release v1.5.0.0**

Run:
```bash
gh release create v1.5.0.0 \
  --target e400f2f \
  --title "v1.5.0.0 — Origin Repository Repointing & Structural Validator" \
  --notes "### Changed
- Repointed documentation and installer to public origin \`savvides/jtbd\`.
- Added \`scripts/validate.py\` structural validator and GitHub Actions CI workflow."
```

- [ ] **Step 2: Create release v1.6.0.0**

Run:
```bash
gh release create v1.6.0.0 \
  --target b12e04b \
  --title "v1.6.0.0 — Claude Code Plugin Conversion" \
  --notes "### Added
- Migrated repository to a first-class Claude Code plugin using \`.claude-plugin/plugin.json\` and \`.claude-plugin/marketplace.json\`."
```

- [ ] **Step 3: Create release v1.6.0.1**

Run:
```bash
gh release create v1.6.0.1 \
  --target de77c45 \
  --title "v1.6.0.1 — Plugin Asset Path & Preamble Fixes" \
  --notes "### Fixed
- Fixed \`/jtbd-demo\` asset resolution under Claude Code plugin installs by probing \`\${CLAUDE_PLUGIN_ROOT}\`.
- Declared \`Bash\` in \`allowed-tools\` for \`/jtbd-demo\` so preamble scripts execute.
- Anchored \`/jtbd-pipeline\` extraction rules to resolved plugin root."
```

- [ ] **Step 4: Create release v1.7.0.0**

Run:
```bash
gh release create v1.7.0.0 \
  --target f5b2af7 \
  --title "v1.7.0.0 — Google Antigravity & Gemini Support" \
  --notes "### Added
- **First-class support for Google Antigravity and Gemini.** jtbd is now dual-compatible with Google Antigravity, Gemini, and Claude Code from a single source of truth:
  - Added \`GEMINI.md\` (and \`AGENTS.md\`) at the repository root, providing Antigravity and Gemini with project instructions, skill listings, schema definitions, and skill routing rules.
  - Added Antigravity plugin manifest and layout under \`plugins/jtbd/plugin.json\` and \`plugins/jtbd/skills/\`.
  - Skill preambles in \`/jtbd-demo\` and \`/jtbd-pipeline\` now probe Antigravity plugin paths (\`~/.gemini/config/plugins/jtbd\`), Claude plugin paths (\`\${CLAUDE_PLUGIN_ROOT}\`), workspace root, and global skill paths.
  - \`validate.py\` now validates \`GEMINI.md\` skill listings alongside \`CLAUDE.md\` and \`README.md\`, and validates that skill preambles probe Antigravity plugin paths in addition to Claude plugin roots."
```

- [ ] **Step 5: Create release v1.8.0.0**

Run:
```bash
gh release create v1.8.0.0 \
  --target 1645577 \
  --title "v1.8.0.0 — Stable Multi-Agent Skills & Voice Polish" \
  --notes "### Changed
- **All 8 skills marked Stable:**
  - \`/jtbd-map\`: Updated schema to emit full YAML representation (\`job\`, \`frequency\`, \`confidence\`, \`steps\`, \`switching_trigger\`, \`forces_summary\`) matching demo data and providing complete input for product briefs.
  - \`/jtbd-brief\`: Standardized input processing to consume the unified Job Map schema directly.
  - \`/jtbd-forces\`: Added explicit layout, typography, CSS Grid, intensity badges, and inferred quote styling rules to ensure reproducible, accessible standalone HTML output.
  - Removed Preview labels and limitations across all documentation.

### Improved
- **Voice and Documentation Quality:**
  - Audited all repository documentation, prompts, guides, and installer scripts with the \`avoid-ai-writing\` rubric to remove AI writing tells, hollow intensifiers, and formulaic constructions.
  - Clear multi-agent positioning across Google Antigravity, Gemini, and Claude Code throughout all documentation."
```

---

### Task 3: Create Current Latest Release (`v1.9.0.0`)

**Files:**
- N/A (Git tags & GitHub Releases)

**Interfaces:**
- Consumes: `main` HEAD commit (`570fbb8` or merge base)
- Produces: Latest GitHub Release `v1.9.0.0`

- [ ] **Step 1: Create latest release v1.9.0.0**

Run:
```bash
gh release create v1.9.0.0 \
  --target main \
  --title "v1.9.0.0 — Formal Schema Specifications & Provenance Tracking" \
  --latest \
  --notes "### Added
- **Formal Schema Specifications (\`docs/schema/\`):**
  - Added JSON/YAML schema definitions for all \`.jtbd/\` artifacts: \`manifest.schema.yml\`, \`switch.schema.yml\`, \`patterns.schema.yml\`, and \`job-map.schema.yml\`.
  - Added \`docs/schema/README.md\` defining data contracts, field definitions, and design goals.
- **Traceable Provenance Metadata:**
  - Added top-level \`provenance\` block (\`skill\`, \`version\`, \`created_at\`) across all generated YAML artifacts and skill templates (\`/jtbd-switch\`, \`/jtbd-patterns\`, \`/jtbd-map\`).

### Changed
- **Unified Schema Versioning:**
  - Standardized on \`schema_version: 1\` across all switch analyses and job maps in addition to manifests and patterns.
- **Validator Enhancements:**
  - \`scripts/validate.py\` now enforces strict schema versioning (\`schema_version: 1\`), top-level key contracts, and \`provenance\` metadata across all \`.jtbd/\` YAML files with expanded self-test coverage."
```

- [ ] **Step 2: Verify release publication**

Run:
```bash
gh release view v1.9.0.0
```
Expected: Displays release v1.9.0.0 details marked as `Latest`.

---

### Task 4: Verification and Local Tag Sync

**Files:**
- N/A

**Interfaces:**
- Consumes: Remote releases and tags
- Produces: Synchronized local tags

- [ ] **Step 1: Fetch all remote tags locally**

Run:
```bash
git fetch --tags origin
```

- [ ] **Step 2: Verify local and remote tags match**

Run:
```bash
git tag -l -n1
gh release list
```

- [ ] **Step 3: Verify repository About overview**

Run:
```bash
gh repo view
```
Expected: All releases listed and repo description/topics verified.
