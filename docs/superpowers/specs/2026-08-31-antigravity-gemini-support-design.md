# Design Spec: Antigravity & Gemini Support for jtbd

**Status:** Approved  
**Date:** 2026-08-31  
**Author:** Antigravity / Philippos Savvides  

---

## 1. Goal

Enable first-class support for Google Antigravity and Gemini in the `jtbd` repository while preserving complete, seamless compatibility with Claude Code. Both agent harnesses will use a single source of truth for skills, schemas, documentation, and validation without requiring build steps or file duplication.

---

## 2. Background & Architecture

Currently, `jtbd` is packaged primarily for Claude Code:
- Skills are defined in root directories (`jtbd-switch/SKILL.md`, `jtbd-demo/SKILL.md`, etc.).
- Project rules and routing instructions are defined in `CLAUDE.md`.
- Claude Code commands are wrapped in `.claude/commands/*.md`.
- Claude Code plugin distribution is managed via `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
- Skill preambles (`jtbd-demo/SKILL.md` and `jtbd-pipeline/SKILL.md`) probe `${CLAUDE_PLUGIN_ROOT}` and `~/.claude/skills/jtbd/`.

### Antigravity & Gemini Integration Model
Antigravity and Gemini support:
1. **Agent Skills format**: Standard `SKILL.md` with YAML frontmatter (`name`, `description`, `allowed-tools`).
2. **Project Rules**: `GEMINI.md` and `AGENTS.md` at workspace root or in `.agents/rules/`.
3. **Customization & Discovery**: Discovered from project workspace, `~/.gemini/config/skills/`, `~/.gemini/config/plugins/`, or declared via `plugins.json` / `skills.json`.

---

## 3. Detailed Technical Design

### 3.1 Project Rule Files (`GEMINI.md` & `AGENTS.md`)
- Add `GEMINI.md` at the repository root.
- Create `AGENTS.md` as a symlink (or exact mirror) of `GEMINI.md` for standard agent compatibility.
- Content of `GEMINI.md`:
  - Skill inventory (all 8 skills: `/jtbd-demo`, `/jtbd-switch`, `/jtbd-interview`, `/jtbd-patterns`, `/jtbd-pipeline`, `/jtbd-forces`, `/jtbd-map`, `/jtbd-brief`).
  - Architecture overview and YAML schemas.
  - Antigravity / Gemini skill routing guidelines.
  - Testing and validation instructions (`python3 scripts/validate.py`).

### 3.2 Skill Preamble Resolution
Update `jtbd-demo/SKILL.md` and `jtbd-pipeline/SKILL.md` preamble bash blocks to probe for both Claude Code and Antigravity/Gemini installation environments:

```bash
_JTBD_SKILLS=""
# 1. Claude Code plugin root
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/jtbd-switch/SKILL.md" ]; then
  _JTBD_SKILLS="$CLAUDE_PLUGIN_ROOT"
# 2. Antigravity plugin paths
elif [ -f "$HOME/.gemini/config/plugins/jtbd/jtbd-switch/SKILL.md" ]; then
  _JTBD_SKILLS="$HOME/.gemini/config/plugins/jtbd"
# 3. Local workspace repository root
elif [ -n "$_ROOT" ] && [ -f "$_ROOT/jtbd-switch/SKILL.md" ]; then
  _JTBD_SKILLS="$_ROOT"
# 4. Antigravity global skill directory
elif [ -f "$HOME/.gemini/config/skills/jtbd/jtbd-switch/SKILL.md" ]; then
  _JTBD_SKILLS="$HOME/.gemini/config/skills/jtbd"
# 5. Pre-v1.6.0.0 legacy clone
elif [ -f "$HOME/.claude/skills/jtbd/jtbd-switch/SKILL.md" ]; then
  _JTBD_SKILLS="$HOME/.claude/skills/jtbd"
fi
```

If demo assets are not found, provide helpful instructions that cover both Claude Code (`/plugin install jtbd@jtbd`) and Antigravity (`~/.gemini/config/plugins/jtbd`).

### 3.3 Antigravity Plugin & Workspace Configuration
- Add `plugins.json` / `skills.json` configuration at repository root if needed, or an Antigravity plugin manifest under `plugins/jtbd/plugin.json` or `.agents/plugins/jtbd/plugin.json`, registering root skills so that cloning or symlinking into `~/.gemini/config/plugins/` automatically registers all 8 skills in Antigravity.

### 3.4 Validator Enhancements (`scripts/validate.py`)
- **`check_docs_list_skills`**:
  - Must validate `GEMINI.md` alongside `CLAUDE.md` and `README.md`.
  - Ensure every skill on disk is documented in `GEMINI.md`.
- **`check_plugin_root_probe`**:
  - Ensure any skill resolving `_JTBD_SKILLS` probes `${CLAUDE_PLUGIN_ROOT}` and `.gemini/config/plugins/`.
- **Self-tests**:
  - Add self-test fixtures asserting that an unadvertised skill in `GEMINI.md` is rejected.
  - Add self-test fixtures asserting that missing Antigravity/Gemini probe paths are rejected.

### 3.5 Documentation Updates
- **`README.md`**:
  - Add section for Antigravity & Gemini usage.
  - Explain how to use `jtbd` in Antigravity CLI and Gemini.
- **`CONTRIBUTING.md`**:
  - Document that adding a skill requires updating `GEMINI.md` in addition to `CLAUDE.md` and `README.md`.
- **`TESTING.md`**:
  - Document `GEMINI.md` validation rules and preamble probe rules.
- **`CHANGELOG.md` & `VERSION`**:
  - Version bump to `1.7.0.0` (MINOR: adds Antigravity and Gemini platform support).
  - Update `CHANGELOG.md`, `VERSION`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`.

---

## 4. Verification & Success Criteria

1. `python3 scripts/validate.py --self-test` passes.
2. `python3 scripts/validate.py` passes across all 8 skills and all doc files (`README.md`, `CLAUDE.md`, `GEMINI.md`, `TESTING.md`, `CONTRIBUTING.md`).
3. `claude plugin validate .claude-plugin/marketplace.json --strict` exits 0.
4. `claude plugin validate .claude-plugin/plugin.json` exits 0.
5. In-repo simulation confirms `GEMINI.md` rules and skill preambles resolve properly under Antigravity / Gemini paths.
