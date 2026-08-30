# TODOS

Open work, grouped by skill, then priority. P0 is most urgent. Completed items move
to the bottom with the version that shipped them.

## jtbd-pipeline

### Unmatched glob aborts the whole `git add`, and the pipeline still reports success
**Priority:** P0
**Found:** v1.5.0.0 pre-landing review (pre-existing, predates v1.4.0.0)

`jtbd-pipeline/SKILL.md:241` runs:

```
git add .jtbd/switches/*.yml .jtbd/patterns/*.yml .jtbd/manifest.yml .jtbd/.gitignore
```

With fewer than 3 transcripts, pattern analysis is skipped, so `.jtbd/patterns/` is
never created. The unmatched glob takes down the entire command. Reproduced in both
shells: bash gives `fatal: pathspec '.jtbd/patterns/*.yml' did not match any files`,
exit 128, empty index; zsh fails before git runs at all. The commit then hits an
empty index and the final summary still reports the pipeline complete.

The user believes their interview evidence was committed. It is untracked.

Fix: glob only what exists, or add paths individually and tolerate misses.

## jtbd-map / jtbd-brief

### The Job Map schema cannot fill the brief that consumes it
**Priority:** P1
**Found:** v1.5.0.0 correctness review — four independent reviewers converged

`jtbd-map/SKILL.md` emits `job:` plus `steps[name/friction/opportunity]`.
`jtbd-brief/SKILL.md` says "Structure the brief exactly like this" and then requires
`## 2. The Forces` and `## 3. Timeline Interventions`. The fields those need
(`forces_summary`, `switching_trigger`) exist in the committed
`demo/.jtbd/jobs/job-01-reliable-numbers-for-leadership.yml` but not in what
`/jtbd-map` instructs Claude to write. On the default path — job map only, user
declines the optional pattern file — half the brief has no source.

Three ways to close it, and the choice is a maintainer call because the demo file is
hand-authored: extend the emitted schema to match the demo file, make the pattern
file read mandatory, or soften "exactly like this".

### Evidence grading is dropped where it matters most
**Priority:** P2
**Found:** v1.5.0.0 correctness review

`jtbd-switch` states the repo's contract: never fabricate a quote, and "it is better
to have gaps than hallucinations". `/jtbd-map` deduces steps with no confidence,
frequency or source attribution, and `/jtbd-brief` turns those steps into feature
proposals. Neither reads the `evidence_gaps` block the patterns file already
produces, so a step covering a known gap arrives in the brief looking exactly like a
3/3-frequency finding.

### Outputs carry PII with no warning
**Priority:** P3
**Found:** v1.5.0.0 correctness review

`.jtbd/forces/` and `.jtbd/briefs/` embed interviewee names, companies and verbatim
quotes. `.jtbd/.gitignore` covers only `raw/`, and neither skill carries the PII
warning `/jtbd-switch` shows before writing.

## Repo

### Skills are prompts, and no eval harness covers them
**Priority:** P2
**Found:** v1.5.0.0 ship

`scripts/validate.py` proves committed example data parses. It cannot check that a
skill's runtime output is any good. `/jtbd-switch` alone carries five extraction
rules and a full YAML output contract that an LLM executes, and an edit to that prose
can degrade every analysis with nothing to catch it.

## Completed

### Every documented install path pointed at a repository that does not exist
**Priority:** was P0
**Completed:** v1.5.0.0 (2026-08-29)

`README.md`, `install.sh` and `jtbd-demo/SKILL.md` pointed at
`github.com/philippossavvides/jtbd`, which returns "Repository not found", so every
install command a user copied failed. Repointed to `github.com/savvides/jtbd`, which
is the repo's actual origin and is public. Verified by running the installer against
a sandboxed HOME: it clones and lands all eight skills.

### install.sh claimed a version it was not installing
**Priority:** was P3
**Completed:** v1.5.0.0 (2026-08-29)

`install.sh` pinned `TAG="v1.1.0"` and printed it, but origin has no tags at all, so
the clone always fell through to the default branch while telling the user it had
installed v1.1.0. The pin is now opt-in via `JTBD_TAG`, the banner states what will
actually be installed, and the fallback announces itself.
