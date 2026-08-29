#!/usr/bin/env python3
"""Structural validation for the jtbd skill collection.

This repo ships Markdown skill definitions and YAML example data, not code, so
there is nothing to unit test. What it does have is a structural contract that
breaks silently: a SKILL.md whose frontmatter does not start at byte 0 loses its
name, description and allowed-tools, and a diff of that file looks fine.

Run with: python3 scripts/validate.py
Self-test: python3 scripts/validate.py --self-test
Exits 0 when every check passes, 1 otherwise.

PyYAML is required, deliberately. An earlier version degraded to a no-op when it
was missing and still printed "All checks passed" — a validator that can pass
without checking is worse than no validator.
"""

import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required for validation. Install it with: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FRONTMATTER = ("name", "version", "description", "allowed-tools")
# Every switch analysis carries these. Verified against examples/expected-output.yml,
# which CONTRIBUTING.md names as the canonical shape, and all four shipped switch files.
SWITCH_KEYS = ("interviewee", "timeline", "forces", "job_story", "evidence_strength")
# A wrapper's first line, which is what the slash-command picker displays.
WRAPPER_LINE1 = re.compile(r"^Read the skill definition at [\w.-]+/SKILL\.md")
# Skill targets referenced from a wrapper. Leading char is not a dot, so "../SKILL.md"
# cannot resolve outside the repo.
SKILL_REF = re.compile(r"\b([A-Za-z0-9_-][\w.-]*)/SKILL\.md")
FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)

failures = []


def fail(path, message):
    failures.append(f"{path}: {message}")


def tracked_files():
    """Tracked files plus untracked-but-not-ignored ones.

    A contributor adding a skill has not staged it yet. Validating only the index
    would stay silent at exactly the moment the check is useful.
    """
    paths = []
    for args in (["git", "ls-files", "-z"],
                 ["git", "ls-files", "-z", "--others", "--exclude-standard"]):
        try:
            out = subprocess.run(args, cwd=ROOT, capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            fail("scripts/validate.py", f"cannot list files ({' '.join(args)}): {exc}")
            return []
        paths += [p for p in out.stdout.decode("utf-8", "replace").split("\0") if p]
    return sorted(set(paths))


def read_text(rel, require_newline=True):
    """Read a repo file as text. Returns None (and records a failure) if unreadable.

    Decodes with errors="replace" so one stray byte reports as a failure line
    instead of a traceback that suppresses every later check.
    """
    path = ROOT / rel
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        fail(rel, "tracked file is missing from the worktree")
        return None
    except OSError as exc:
        fail(rel, f"cannot read: {exc}")
        return None
    if require_newline and not raw.endswith(b"\n"):
        fail(rel, "missing trailing newline")
    return raw.decode("utf-8", "replace")


def parse_frontmatter(text):
    """Return (block, error). error is None, 'not_at_start', or 'unterminated'.

    Both delimiters must be alone on their line, so a horizontal rule or a setext
    underline in the body cannot masquerade as the closing fence.
    """
    match = FRONTMATTER.match(text)
    if match:
        return match.group(1), None
    if not text.startswith("---"):
        return None, "not_at_start"
    return None, "unterminated"


def check_skills(files, skill_dirs):
    """Frontmatter is positioned, parseable, complete, and names its own directory."""
    skills = sorted(f for f in files if f.endswith("/SKILL.md"))
    if not skills:
        fail("SKILL.md", "no skill definitions found")
        return 0

    for rel in skills:
        directory = rel.rsplit("/", 1)[0].rsplit("/", 1)[-1]
        text = read_text(rel)
        if text is None:
            continue

        block, error = parse_frontmatter(text)
        if error == "not_at_start":
            first = text.splitlines()[0] if text.splitlines() else ""
            fail(rel, f"YAML frontmatter must start at byte 0, found: {first!r}")
            continue
        if error == "unterminated":
            fail(rel, "YAML frontmatter is never closed by a '---' line of its own")
            continue

        try:
            meta = yaml.safe_load(block)
        except yaml.YAMLError as exc:
            fail(rel, f"frontmatter is not valid YAML ({yaml_where(exc)})")
            continue

        if not isinstance(meta, dict):
            fail(rel, f"frontmatter parsed to {type(meta).__name__}, expected a mapping")
            continue

        for key in REQUIRED_FRONTMATTER:
            if key not in meta:
                fail(rel, f"frontmatter is missing required key '{key}'")

        if meta.get("name") != directory:
            fail(rel, f"frontmatter name {meta.get('name')!r} != directory {directory!r}")

    return len(skills)


def check_commands(files, skill_dirs):
    """Each wrapper is paired with the skill its filename names."""
    commands = sorted(f for f in files if f.startswith(".claude/commands/") and f.endswith(".md"))
    paired = set()

    for rel in commands:
        stem = rel.rsplit("/", 1)[-1][: -len(".md")]
        text = read_text(rel)
        if text is None:
            continue

        lines = text.splitlines()
        if not lines or not WRAPPER_LINE1.match(lines[0]):
            first = lines[0] if lines else ""
            fail(rel, f"line 1 must start 'Read the skill definition at <skill>/SKILL.md', found: {first!r}")

        referenced = SKILL_REF.findall(text)
        if not referenced:
            fail(rel, "does not reference any SKILL.md")
            continue

        for target in referenced:
            if not (ROOT / target / "SKILL.md").is_file():
                fail(rel, f"references {target}/SKILL.md, which does not exist")

        # Coverage is not pairing: a wrapper must point at the skill its own
        # filename names, or the slash command runs a different skill entirely.
        if stem not in referenced:
            fail(rel, f"wrapper is named for {stem!r} but references {sorted(set(referenced))}")
        else:
            paired.add(stem)

    for directory in sorted(skill_dirs - paired):
        fail(f"{directory}/SKILL.md", f"has no wrapper at .claude/commands/{directory}.md")

    return len(commands)


def yaml_where(exc):
    """Locate a YAML error without echoing the source line.

    PyYAML's str() embeds a verbatim snippet. The .jtbd/ files hold customer
    interview quotes, and CI logs outlive the file they came from.
    """
    mark = getattr(exc, "problem_mark", None)
    if mark is not None:
        return f"{type(exc).__name__} at line {mark.line + 1}, column {mark.column + 1}"
    return type(exc).__name__


def check_yaml(files, skill_dirs):
    """Shipped YAML parses, and switch analyses carry their documented keys."""
    targets = sorted(f for f in files if f.endswith((".yml", ".yaml")))
    for rel in targets:
        text = read_text(rel, require_newline=False)
        if text is None:
            continue
        try:
            doc = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            fail(rel, f"does not parse ({yaml_where(exc)})")
            continue

        if "/switches/" in rel or rel == "examples/expected-output.yml":
            if not isinstance(doc, dict):
                fail(rel, "switch analysis must be a mapping")
                continue
            for key in SWITCH_KEYS:
                if key not in doc:
                    fail(rel, f"switch analysis is missing top-level '{key}'")

    return len(targets)


def check_availability(files, skill_dirs):
    """A skill that ships is never advertised as unavailable.

    Matches any line pairing a shipped skill with 'coming soon', in either order
    and any punctuation. The release step this guards is a README table cell
    ('| Coming soon |'), not only the parenthesized prose form.
    """
    docs = sorted(f for f in files if f.endswith(".md"))
    for rel in docs:
        if rel.startswith("docs/superpowers/"):
            continue  # dated plans and specs are a historical record
        text = read_text(rel, require_newline=False)
        if text is None:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if "coming soon" not in line.lower():
                continue
            for skill in sorted(skill_dirs):
                if skill in line:
                    fail(f"{rel}:{number}", f"{skill} ships in this repo but is marked 'coming soon'")
    return len(docs)


def check_docs_list_skills(files, skill_dirs):
    """Every shipped skill is advertised where users look for it."""
    for rel in ("README.md", "CLAUDE.md"):
        text = read_text(rel, require_newline=False)
        if text is None:
            continue
        for skill in sorted(skill_dirs):
            if f"/{skill}" not in text:
                fail(rel, f"ships {skill} but never lists it")
    return 2


def self_test():
    """Prove the pure helpers still reject what they were written to reject."""
    good = "---\nname: jtbd-map\nversion: 1.0.0\n---\n\n## Preamble\n"
    block, error = parse_frontmatter(good)
    assert error is None and "name: jtbd-map" in block, "rejected valid frontmatter"

    for bad, kind in [
        ("\n---\nname: x\n---\n", "not_at_start"),
        ("<!-- leaked -->\n---\nname: x\n---\n", "not_at_start"),
        ("---\nname: x\n", "unterminated"),
        ("---\nname: x\n--- not a close\n", "unterminated"),
        ("---\nname: x\n-----------\n", "unterminated"),
    ]:
        block, error = parse_frontmatter(bad)
        assert block is None and error == kind, f"accepted {bad!r} (got {error!r}, want {kind!r})"

    for line in ["", "<!-- x -->", "# heading", "  Read the skill definition at a/SKILL.md"]:
        assert not WRAPPER_LINE1.match(line), f"accepted bad wrapper line 1: {line!r}"
    assert WRAPPER_LINE1.match("Read the skill definition at jtbd-map/SKILL.md and execute it.")

    assert SKILL_REF.findall("see jtbd-map/SKILL.md") == ["jtbd-map"]
    assert ".." not in SKILL_REF.findall("see ../SKILL.md"), "regex allows parent traversal"

    print("self-test ok")
    return 0


CHECKS = (check_skills, check_commands, check_yaml, check_availability, check_docs_list_skills)


def main():
    if "--self-test" in sys.argv:
        return self_test()

    files = tracked_files()
    if not files:
        print("FAILED (1):\n  - " + failures[0])
        return 1

    skill_dirs = {f.rsplit("/", 1)[0].rsplit("/", 1)[-1]
                  for f in files if f.endswith("/SKILL.md")}

    print("Validating jtbd skill collection...")
    inspected = sum(check(files, skill_dirs) for check in CHECKS)
    print(f"  {len(skill_dirs)} skills, {inspected} files inspected")

    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
