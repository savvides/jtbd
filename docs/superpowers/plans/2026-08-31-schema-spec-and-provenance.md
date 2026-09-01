# Plan: Schema Specification, Unified Versioning & Provenance Tracking

## Problem Statement
The `.jtbd/` schema currently lives primarily as prompt text inside skills. `manifest.yml` and `patterns` files carry `schema_version: 1`, while switch analyses and job maps omit `schema_version`. Furthermore, generated files lack reproducible metadata (`generated_by`, `skill_version`, date), and `scripts/validate.py` checks basic key tuples rather than documented schemas.

---

## Technical Specifications & Data Architecture

### 1. Schema Definitions (`docs/schema/`)
Create formal YAML schema reference files under `docs/schema/`:
- `docs/schema/manifest.schema.yml`: Defines `schema_version`, `title`, `description`, `created_at`, `interviews`.
- `docs/schema/switch.schema.yml`: Defines `schema_version`, `provenance`, `interviewee`, `timeline` (first_thought, passive_looking, active_looking, deciding, outcome), `forces` (push, pull, anxiety, habit), `job_story` (when, want_to, so_i_can), `evidence_strength`.
- `docs/schema/patterns.schema.yml`: Defines `schema_version`, `provenance`, `analyzed_at`, `sources`, `jobs` (name, count, evidence, description), `cross_cutting_forces`.
- `docs/schema/job-map.schema.yml`: Defines `schema_version`, `provenance`, `job`, `frequency`, `confidence`, `steps` (name, friction, opportunity), `switching_trigger`, `forces_summary` (what_pushes, what_pulls, what_scares, what_holds).
- `docs/schema/README.md`: Complete human and agent reference guide explaining schema semantics, versioning policy, and required vs optional fields.

### 2. Standardize `schema_version: 1`
All YAML artifacts across `.jtbd/` must explicitly declare `schema_version: 1`:
- Switch analyses (`.jtbd/switches/*.yml`, `demo/.jtbd/switches/*.yml`)
- Patterns (`.jtbd/patterns.yml`, `demo/.jtbd/patterns.yml`)
- Job Maps (`.jtbd/jobs/*.yml`, `demo/.jtbd/jobs/*.yml`)
- Manifest (`.jtbd/manifest.yml`, `demo/.jtbd/manifest.yml`)

### 3. Provenance Metadata
All generated YAML files include a top-level `provenance` block:
```yaml
schema_version: 1
provenance:
  skill: "jtbd-switch"
  version: "1.8.0.0"
  created_at: "2026-08-31"
```

### 4. Validator Enhancements (`scripts/validate.py`)
- Check schema conformity for all `.jtbd/` YAML files against documented required keys and types.
- Validate that `schema_version` is present and equals `1`.
- Validate that `provenance` metadata is present and valid.
- Expand `--self-test` to test schema validation errors (missing `schema_version`, invalid field types, missing required blocks).

---

## Step-by-Step Execution Plan

### Step 1: Create Schema Specification Files (`docs/schema/`)
- Write `docs/schema/README.md`.
- Write `docs/schema/manifest.schema.yml`, `docs/schema/switch.schema.yml`, `docs/schema/patterns.schema.yml`, `docs/schema/job-map.schema.yml`.

### Step 2: Update Skill Output Formats
- Update `jtbd-switch/SKILL.md` to include `schema_version: 1` and `provenance` block.
- Update `jtbd-patterns/SKILL.md` to include `schema_version: 1` and `provenance` block.
- Update `jtbd-map/SKILL.md` to include `schema_version: 1` and `provenance` block.

### Step 3: Update Existing Data Fixtures
- Update `demo/.jtbd/switches/*.yml` with `schema_version: 1` and `provenance`.
- Update `demo/.jtbd/patterns.yml` with `schema_version: 1` and `provenance`.
- Update `demo/.jtbd/jobs/*.yml` with `schema_version: 1` and `provenance`.
- Update `examples/expected-output.yml` with `schema_version: 1` and `provenance`.
- Update `.jtbd/switches/*.yml` with `schema_version: 1` and `provenance`.

### Step 4: Upgrade `scripts/validate.py`
- Add rigorous schema validation for switch, pattern, job-map, and manifest files.
- Add self-test cases in `validate.py --self-test` verifying that invalid schemas are caught and rejected.

### Step 5: Verification & Documentation Updates
- Run `python3 scripts/validate.py --self-test` and `python3 scripts/validate.py`.
- Update `TODOS.md` moving completed schema items to `## Completed`.
- Update `TESTING.md` documenting schema validation rules.
- Run `claude plugin validate` checks.

---

## GSTACK REVIEW REPORT

### Review Summary
- **CEO Review**: Approved (Selective Expansion & Completeness). Establishes formal data contracts and reproducibility.
- **DX Review**: Approved (Score: 10/10). Developers inspecting or interoperating with `jtbd` have clear schema documentation in `docs/schema/` and descriptive validator errors.
- **Eng Review**: Approved. Clean architecture with zero external runtime dependencies. Backward-compatible `schema_version: 1` unification.

### Auto-Decisions Audit Trail
1. *Schema Format*: Pure YAML schema reference files under `docs/schema/` with zero external dependencies (Principle 5: Explicit over clever, Principle 3: Pragmatic).
2. *Version Unification*: Adopt `schema_version: 1` across all files to match `manifest.yml` and `patterns.yml` (Principle 4: DRY, Principle 1: Completeness).
3. *Provenance Contract*: Require `skill`, `version`, and `created_at` (Principle 1: Completeness, Principle 2: Boil lakes).
4. *Self-Test Coverage*: Add negative schema test fixtures in `scripts/validate.py --self-test` (Principle 1: Completeness).

### Status
**READY FOR IMPLEMENTATION**
