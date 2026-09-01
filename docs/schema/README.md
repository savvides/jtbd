# Jobs to Be Done Schema Specification

This directory defines the formal YAML data contracts used by `jtbd` across all skills and workflows.

## Design Goals

1. **Version Controlled**: All user-facing data files live in `.jtbd/` within the user repository.
2. **Deterministic & Versioned**: Every file carries a top-level `schema_version: 1` field to allow safe schema evolution.
3. **Traceable Provenance**: Every generated file records reproducible metadata in a `provenance` block (`skill`, `version`, `created_at`).
4. **Zero Dependencies**: Schemas are plain YAML/JSON Schema definitions that can be validated offline by `scripts/validate.py`.

---

## Artifact Schemas

| File Type | Default Path | Schema Specification | Description |
|---|---|---|---|
| **Manifest** | `.jtbd/manifest.yml` | [`manifest.schema.yml`](file:///Users/philippossavvides/github/jtbd/docs/schema/manifest.schema.yml) | Project-level interview index and metadata |
| **Switch Analysis** | `.jtbd/switches/*.yml` | [`switch.schema.yml`](file:///Users/philippossavvides/github/jtbd/docs/schema/switch.schema.yml) | Moesta timeline and Four Forces analysis for a single interview |
| **Patterns Synthesis** | `.jtbd/patterns.yml` | [`patterns.schema.yml`](file:///Users/philippossavvides/github/jtbd/docs/schema/patterns.schema.yml) | Cross-interview synthesis and clustered jobs across 3+ interviews |
| **Job Map** | `.jtbd/jobs/*.yml` | [`job-map.schema.yml`](file:///Users/philippossavvides/github/jtbd/docs/schema/job-map.schema.yml) | Structured chronological step-by-step job map with friction and opportunities |

---

## Provenance Block Specification

All generated artifacts contain a top-level `provenance` dictionary:

```yaml
provenance:
  skill: "jtbd-switch"     # Name of the skill that created or updated the artifact
  version: "1.8.0.0"       # Version of the jtbd skill suite used
  created_at: "YYYY-MM-DD" # ISO 8601 creation date (UTC)
```
