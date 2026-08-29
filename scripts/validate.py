#!/usr/bin/env python3
"""Structural validation for the jtbd skill collection.

This repo ships Markdown skill definitions and YAML example data, not code, so
there is nothing to unit test. What it does have is a structural contract that
breaks silently: a SKILL.md whose frontmatter does not start at byte 0 loses its
name, description and allowed-tools, and a diff of that file looks fine.

Run with: python3 scripts/validate.py
Exits 0 when every check passes, 1 otherwise.
"""

import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    yaml = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED_FRONTMATTER = ("name", "version", "description", "allowed-tools")

failures = []
checks_run = 0


def fail(path, message):
    failures.append(f"{path}: {message}")


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return out.stdout.splitlines()


def read_bytes(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return fh.read()


def split_frontmatter(text):
    """Return the frontmatter block, or None if it is not at byte 0."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end]


def check_skills(files):
    """Every <skill>/SKILL.md parses and declares what the loader needs."""
    global checks_run
    skills = sorted(f for f in files if re.fullmatch(r"[^/]+/SKILL\.md", f))
    if not skills:
        fail("SKILL.md", "no skill definitions found")
        return []

    for rel in skills:
        checks_run += 1
        raw = read_bytes(rel)
        directory = rel.split("/")[0]

        if not raw.endswith(b"\n"):
            fail(rel, "missing trailing newline")

        text = raw.decode("utf-8")
        block = split_frontmatter(text)
        if block is None:
            first = text.splitlines()[0] if text.splitlines() else ""
            fail(rel, f"YAML frontmatter must start at byte 0, found: {first!r}")
            continue

        if yaml is None:
            continue

        try:
            meta = yaml.safe_load(block)
        except yaml.YAMLError as exc:
            fail(rel, f"frontmatter is not valid YAML: {exc}")
            continue

        if not isinstance(meta, dict):
            fail(rel, "frontmatter did not parse to a mapping")
            continue

        for key in REQUIRED_FRONTMATTER:
            if key not in meta:
                fail(rel, f"frontmatter is missing required key '{key}'")

        if meta.get("name") != directory:
            fail(rel, f"frontmatter name {meta.get('name')!r} != directory {directory!r}")

    return skills


def check_commands(files, skills):
    """Every command wrapper points at a real SKILL.md, and carries nothing else."""
    global checks_run
    commands = sorted(f for f in files if f.startswith(".claude/commands/"))
    skill_dirs = {s.split("/")[0] for s in skills}
    wired = set()

    for rel in commands:
        checks_run += 1
        raw = read_bytes(rel)
        if not raw.endswith(b"\n"):
            fail(rel, "missing trailing newline")

        text = raw.decode("utf-8")
        lines = text.splitlines()
        if lines and lines[0].lstrip().startswith("<!--"):
            fail(rel, f"stray comment on line 1 leaks into the command picker: {lines[0]!r}")

        referenced = re.findall(r"([\w.-]+)/SKILL\.md", text)
        if not referenced:
            fail(rel, "does not reference any SKILL.md")
            continue

        for target in referenced:
            wired.add(target)
            if not os.path.exists(os.path.join(ROOT, target, "SKILL.md")):
                fail(rel, f"references {target}/SKILL.md, which does not exist")

    missing = skill_dirs - wired
    for directory in sorted(missing):
        fail(f"{directory}/SKILL.md", "has no wrapper in .claude/commands/")

    return skill_dirs


def check_yaml(files):
    """Every shipped YAML file parses. Generated evidence must stay machine-readable."""
    global checks_run
    if yaml is None:
        print("  ! pyyaml not installed, skipping YAML parse checks")
        return
    for rel in sorted(f for f in files if f.endswith((".yml", ".yaml"))):
        checks_run += 1
        try:
            yaml.safe_load(read_bytes(rel).decode("utf-8"))
        except yaml.YAMLError as exc:
            fail(rel, f"does not parse: {exc}")


def check_no_stale_coming_soon(files, skill_dirs):
    """A skill that exists must never be advertised as unavailable."""
    global checks_run
    pattern = re.compile(r"`?/(?P<skill>jtbd-[a-z]+)`?[^\n]{0,120}?\(coming soon\)", re.I)
    for rel in sorted(f for f in files if f.endswith(".md")):
        if rel.startswith("docs/superpowers/"):
            continue  # dated plans and specs are a historical record
        checks_run += 1
        text = read_bytes(rel).decode("utf-8", errors="replace")
        for match in pattern.finditer(text):
            skill = match.group("skill")
            if skill in skill_dirs:
                line = text[: match.start()].count("\n") + 1
                fail(f"{rel}:{line}", f"{skill} is marked '(coming soon)' but ships in this repo")


def main():
    files = tracked_files()
    print("Validating jtbd skill collection...")
    skills = check_skills(files)
    skill_dirs = check_commands(files, skills)
    check_yaml(files)
    check_no_stale_coming_soon(files, skill_dirs)

    print(f"  {len(skills)} skills, {checks_run} checks")
    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
