# Antigravity & Gemini Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement first-class support for Google Antigravity and Gemini in the `jtbd` repository alongside Claude Code, using a single source of truth for all skills, manifests, rules, and validators.

**Architecture:** Add `GEMINI.md` and `AGENTS.md` at repo root for Antigravity/Gemini project context; update skill preambles to resolve assets across Claude and Antigravity environments; add Antigravity plugin manifest; update `scripts/validate.py` to enforce documentation parity and dual probes; update repo documentation and bump version.

**Tech Stack:** Python 3 (validator & self-test), Markdown (Agent Skills, GEMINI.md, AGENTS.md), JSON (plugin manifests), Bash (preambles).

**Spec:** `docs/superpowers/specs/2026-08-31-antigravity-gemini-support-design.md`

## Global Constraints
- No build steps or compiled binaries.
- Skills must follow standard Agent Skills specification with valid YAML frontmatter (`name`, `description`, `allowed-tools`).
- `scripts/validate.py` must pass with zero errors, and `python3 scripts/validate.py --self-test` must pass.
- `claude plugin validate` must pass for both manifests.
- Every commit must be atomic, focused, and verified.

---

### Task 1: Create `GEMINI.md` and `AGENTS.md`

**Files:**
- Create: `GEMINI.md`
- Create: `AGENTS.md` (or symlink to `GEMINI.md`)

**Interfaces:**
- Consumes: Skill directories (`jtbd-*/SKILL.md`), `CLAUDE.md`, `examples/expected-output.yml`
- Produces: Project-level instructions, skill routing table, YAML schema reference, and contributor instructions for Antigravity & Gemini

- [ ] **Step 1: Write `GEMINI.md`**
Create `GEMINI.md` containing project purpose, skill list (all 8 skills), Preview designations, Architecture, YAML Schema, Skill Routing rules for Antigravity/Gemini, and Testing guidelines.

- [ ] **Step 2: Create `AGENTS.md`**
Create `AGENTS.md` linking or matching `GEMINI.md` for standard agent tooling compatibility.

- [ ] **Step 3: Verify content against `CLAUDE.md`**
Ensure all 8 skills (`/jtbd-demo`, `/jtbd-switch`, `/jtbd-interview`, `/jtbd-patterns`, `/jtbd-pipeline`, `/jtbd-forces`, `/jtbd-map`, `/jtbd-brief`) match names and routing triggers.

- [ ] **Step 4: Commit**
```bash
git add GEMINI.md AGENTS.md
git commit -m "feat: add GEMINI.md and AGENTS.md for Antigravity and Gemini support"
```

---

### Task 2: Update Validator (`scripts/validate.py`) for Dual Documentation & Probe Checks

**Files:**
- Modify: `scripts/validate.py`

**Interfaces:**
- Consumes: `GEMINI.md`, `CLAUDE.md`, `README.md`, `*/SKILL.md`
- Produces: Enhanced `check_docs_list_skills`, enhanced `check_plugin_root_probe`, and new self-test fixtures

- [ ] **Step 1: Write failing self-test in `scripts/validate.py`**
Add self-test assertions requiring `GEMINI.md` to list every skill, and requiring `_JTBD_SKILLS` resolvers to probe both `CLAUDE_PLUGIN_ROOT` and `.gemini/config/plugins`.

- [ ] **Step 2: Run `python3 scripts/validate.py --self-test` to verify it fails**
Confirm the new self-test assertions fail on current code.

- [ ] **Step 3: Implement validation logic in `scripts/validate.py`**
Update `check_docs_list_skills` to check `GEMINI.md` alongside `CLAUDE.md`.
Update `check_plugin_root_probe` to verify `.gemini/config/plugins` is probed in skills that resolve `_JTBD_SKILLS`.

- [ ] **Step 4: Run `python3 scripts/validate.py --self-test` to verify it passes**
Run self-test and verify all fixtures pass.

- [ ] **Step 5: Commit**
```bash
git add scripts/validate.py
git commit -m "feat(validate): check GEMINI.md skill listing and Antigravity preamble probes"
```

---

### Task 3: Update Skill Preambles in `jtbd-demo` and `jtbd-pipeline`

**Files:**
- Modify: `jtbd-demo/SKILL.md`
- Modify: `jtbd-pipeline/SKILL.md`

**Interfaces:**
- Consumes: Antigravity plugin paths, Claude plugin paths, workspace paths
- Produces: Dual-platform asset and skill location resolution

- [ ] **Step 1: Update `jtbd-demo/SKILL.md`**
Update the preamble bash block to probe:
1. `${CLAUDE_PLUGIN_ROOT}`
2. `$HOME/.gemini/config/plugins/jtbd`
3. `$_ROOT` (git workspace root)
4. `$HOME/.gemini/config/skills/jtbd`
5. `$HOME/.claude/skills/jtbd`
Update asset not-found message to provide instructions for both Claude Code and Antigravity users.

- [ ] **Step 2: Update `jtbd-pipeline/SKILL.md`**
Update the preamble bash block to follow the identical probe order, checking for `jtbd-switch/SKILL.md` at each location.

- [ ] **Step 3: Run validator**
```bash
python3 scripts/validate.py --self-test && python3 scripts/validate.py
```
Expected: All checks pass.

- [ ] **Step 4: Commit**
```bash
git add jtbd-demo/SKILL.md jtbd-pipeline/SKILL.md
git commit -m "fix(preamble): add Antigravity plugin and skill paths to resolver"
```

---

### Task 4: Add Antigravity Plugin Configuration

**Files:**
- Create: `plugins/jtbd/plugin.json` or root `plugins.json`

**Interfaces:**
- Consumes: Root skills
- Produces: Antigravity plugin registration manifest

- [ ] **Step 1: Write Antigravity plugin manifest**
Add `plugins/jtbd/plugin.json` (or declared config) specifying the plugin name and description so Antigravity CLI and Gemini recognize the plugin when installed in `~/.gemini/config/plugins/jtbd` or referenced in workspace.

- [ ] **Step 2: Verify plugin discovery**
Check that files parse as valid JSON.

- [ ] **Step 3: Commit**
```bash
git add plugins/
git commit -m "feat: add Antigravity plugin manifest"
```

---

### Task 5: Update Documentation & Version Bump

**Files:**
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `TESTING.md`
- Modify: `TODOS.md`
- Modify: `CHANGELOG.md`
- Modify: `VERSION`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: All updated components
- Produces: Synchronized documentation, release changelog, and version 1.7.0.0

- [ ] **Step 1: Update `README.md`**
Add Antigravity CLI and Gemini installation and usage instructions alongside Claude Code.

- [ ] **Step 2: Update `CONTRIBUTING.md` and `TESTING.md`**
Document `GEMINI.md` maintenance, dual-agent testing, and validator rules.

- [ ] **Step 3: Update `TODOS.md`**
Add note on Antigravity / Gemini testing and verification.

- [ ] **Step 4: Update `VERSION`, `CHANGELOG.md`, `plugin.json`, `marketplace.json`**
Bump version to `1.7.0.0`. Document changes in `CHANGELOG.md`.

- [ ] **Step 5: Run full validation suite**
```bash
python3 scripts/validate.py --self-test && python3 scripts/validate.py && claude plugin validate .claude-plugin/marketplace.json --strict && claude plugin validate .claude-plugin/plugin.json
```
Expected: All pass.

- [ ] **Step 6: Commit**
```bash
git add README.md CONTRIBUTING.md TESTING.md TODOS.md CHANGELOG.md VERSION .claude-plugin/
git commit -m "chore: bump version to 1.7.0.0 and update docs for Antigravity support"
```

---

### Task 6: Final Verification, Code Review & PR

**Files:**
- All touched files

- [ ] **Step 1: Run comprehensive local test & validation suite**
- [ ] **Step 2: Push branch to GitHub**
- [ ] **Step 3: Create PR using `gh pr create`**
- [ ] **Step 4: Conduct independent code review**
- [ ] **Step 5: Verify CI checks on GitHub**
- [ ] **Step 6: Execute merge per user goal**
