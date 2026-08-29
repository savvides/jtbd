#!/usr/bin/env python3
"""Structural validation for the jtbd skill collection.

This repo ships Markdown skill definitions and YAML example data, not code, so
there is nothing to unit test. What it does have is a structural contract that
breaks silently: a SKILL.md whose frontmatter does not start at byte 0 loses its
name, description and allowed-tools, and a diff of that file looks fine.

Run with: python3 scripts/validate.py
Self-test: python3 scripts/validate.py --self-test
Exits 0 when every check passes, 1 otherwise.

Two properties are deliberate, because both were bugs here once:
PyYAML is required rather than optional, and the self-test reports failures
explicitly rather than through `assert` (which -O strips). A validator that can
pass without checking is worse than no validator.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required for validation. Install it with: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FRONTMATTER = ("name", "version", "description", "allowed-tools")
# A skill is a top-level directory holding a SKILL.md. Wrappers reference a single
# path segment, so a nested SKILL.md could never satisfy the pairing check.
SKILL_PATH = re.compile(r"[^/]+/SKILL\.md")
# A wrapper's first line: what the picker displays, and what decides which skill
# actually runs. The group is the target, and cannot begin with a dot.
WRAPPER_LINE1 = re.compile(r"^Read the skill definition at ([A-Za-z0-9_-][\w.-]*)/SKILL\.md")
SKILL_REF = re.compile(r"\b([A-Za-z0-9_-][\w.-]*)/SKILL\.md")
FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)
# Prose describing a past availability state, rather than advertising a current one.
PAST_TENSE = re.compile(r"no longer|previously|used to be|was marked|removed the", re.I)
SEGMENT = re.compile(r"[|.]")
ALLOW_MARKER = "<!-- validate: allow-coming-soon -->"

# Documented shapes. A document is classified by its own content where possible,
# so a non-switch file living under switches/ is not forced into the wrong contract.
SWITCH_KEYS = ("interviewee", "timeline", "forces", "job_story", "evidence_strength")
PATTERNS_KEYS = ("schema_version", "clusters", "force_patterns")
JOB_KEYS = ("job", "steps")
MANIFEST_KEYS = ("schema_version", "product", "target_user", "settings")

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
    """Read a repo file as text, or record a failure and return None.

    Decodes with errors="replace" so one stray byte reports as a failure line
    instead of a traceback that suppresses every later check.
    """
    try:
        raw = (ROOT / rel).read_bytes()
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
    """Return (block, error): error is None, 'not_at_start', or 'unterminated'.

    Both delimiters must be alone on their line, so a horizontal rule or a setext
    underline in the body cannot masquerade as the closing fence.
    """
    match = FRONTMATTER.match(text)
    if match:
        return match.group(1), None
    return (None, "not_at_start") if not text.startswith("---") else (None, "unterminated")


def yaml_where(exc):
    """Locate a YAML error without echoing the source line.

    PyYAML's str() embeds a verbatim snippet. The .jtbd/ files hold customer
    interview quotes, and CI logs outlive the file they came from.
    """
    mark = getattr(exc, "problem_mark", None)
    if mark is not None:
        return f"{type(exc).__name__} at line {mark.line + 1}, column {mark.column + 1}"
    return type(exc).__name__


def skill_paths(files):
    return sorted(f for f in files if SKILL_PATH.fullmatch(f))


def check_skills(files, skill_dirs):
    """Frontmatter is positioned, parseable, complete, and names its own directory."""
    read = set()
    skills = skill_paths(files)
    if not skills:
        fail("SKILL.md", "no skill definitions found")
        return read

    for rel in skills:
        directory = rel.split("/")[0]
        text = read_text(rel)
        if text is None:
            continue
        read.add(rel)

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

    return read


def check_commands(files, skill_dirs):
    """Each wrapper is paired, by its line 1, with the skill its filename names."""
    read, paired = set(), set()
    commands = sorted(f for f in files
                      if f.startswith(".claude/commands/") and f.endswith(".md"))

    for rel in commands:
        stem = rel.rsplit("/", 1)[-1][: -len(".md")]
        text = read_text(rel)
        if text is None:
            continue
        read.add(rel)

        lines = text.splitlines()
        head = WRAPPER_LINE1.match(lines[0]) if lines else None
        if head is None:
            first = lines[0] if lines else ""
            fail(rel, f"line 1 must start 'Read the skill definition at <skill>/SKILL.md', found: {first!r}")
            continue

        for target in sorted(set(SKILL_REF.findall(text))):
            if not (ROOT / target / "SKILL.md").is_file():
                fail(rel, f"references {target}/SKILL.md, which does not exist")

        # Pair on line 1 specifically. A mention lower in the body does not decide
        # which skill runs, so scanning the whole file would pass a wrapper whose
        # first line points somewhere else.
        if head.group(1) != stem:
            fail(rel, f"wrapper is named for {stem!r} but line 1 runs {head.group(1)!r}")
        else:
            paired.add(stem)

    for directory in sorted(skill_dirs - paired):
        fail(f"{directory}/SKILL.md", f"has no wrapper at .claude/commands/{directory}.md")

    return read


def classify_yaml(rel, doc):
    """Name the documented shape this file must satisfy, or None."""
    if not isinstance(doc, dict):
        return None
    if "interviewee" in doc or "/switches/" in rel or rel == "examples/expected-output.yml":
        return "switch", SWITCH_KEYS
    if rel.endswith("manifest.yml"):
        return "manifest", MANIFEST_KEYS
    if "/patterns/" in rel or "clusters" in doc:
        return "patterns", PATTERNS_KEYS
    if "/jobs/" in rel or "steps" in doc:
        return "job map", JOB_KEYS
    return None


def check_yaml(files, skill_dirs):
    """Shipped YAML parses and carries the keys its shape documents."""
    read = set()
    for rel in sorted(f for f in files if f.endswith((".yml", ".yaml"))):
        if rel.startswith(".github/"):
            continue  # workflow schema is GitHub's to enforce
        text = read_text(rel, require_newline=False)
        if text is None:
            continue
        read.add(rel)
        try:
            doc = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            fail(rel, f"does not parse ({yaml_where(exc)})")
            continue

        shape = classify_yaml(rel, doc)
        if shape is None:
            continue
        label, keys = shape
        for key in keys:
            if key not in doc:
                fail(rel, f"{label} is missing top-level '{key}'")
    return read


def check_availability(files, skill_dirs):
    """A skill that ships is never advertised as unavailable.

    Matches any line pairing a shipped skill with 'coming soon', in either order.
    The release step this guards is a README table cell, not only prose.
    """
    read = set()
    for rel in sorted(f for f in files if f.endswith(".md")):
        # Historical records describe past states by design.
        if rel.startswith("docs/superpowers/") or rel == "CHANGELOG.md":
            continue
        text = read_text(rel, require_newline=False)
        if text is None:
            continue
        read.add(rel)
        for number, line in enumerate(text.splitlines(), 1):
            if "coming soon" not in line.lower():
                continue
            # Scope the past-tense escape to the segment holding the phrase. A
            # neighbouring table cell or clause must not defuse a live claim.
            segment = next((s for s in SEGMENT.split(line) if "coming soon" in s.lower()), line)
            if ALLOW_MARKER in line or PAST_TENSE.search(segment):
                continue
            for skill in sorted(skill_dirs):
                if skill in line:
                    fail(f"{rel}:{number}",
                         f"{skill} ships in this repo but is marked 'coming soon'")
    return read


def check_docs_list_skills(files, skill_dirs):
    """Every shipped skill is advertised where users look for it."""
    read = set()
    for rel in (r for r in files if r in {"README.md", "CLAUDE.md"}):
        text = read_text(rel, require_newline=False)
        if text is None:
            continue
        read.add(rel)
        for skill in sorted(skill_dirs):
            if f"/{skill}" not in text:
                fail(rel, f"ships {skill} but never lists it")
    for rel in {"README.md", "CLAUDE.md"} - read:
        fail(rel, "is missing, so skill listings cannot be verified")
    return read


CHECKS = (check_skills, check_commands, check_yaml, check_availability, check_docs_list_skills)


def run_checks(files):
    skill_dirs = {f.split("/")[0] for f in skill_paths(files)}
    read = set()
    for check in CHECKS:
        read |= check(files, skill_dirs)
    return read


# ---------------------------------------------------------------- self-test

WRAPPER = "Read the skill definition at {name}/SKILL.md and execute it exactly as specified.\n"
SKILL = "---\nname: {name}\nversion: 1.0.0\ndescription: d\nallowed-tools:\n  - Bash\n---\n\nbody\n"


def _base_fixture():
    return {
        "alpha/SKILL.md": SKILL.format(name="alpha"),
        ".claude/commands/alpha.md": WRAPPER.format(name="alpha"),
        "README.md": "| `/alpha` | Available |\n",
        "CLAUDE.md": "- `/alpha` does things\n",
    }


def _run_fixture(files_map):
    """Build a throwaway repo, run every check against it, return its failures."""
    global ROOT, failures
    saved_root, saved_failures = ROOT, failures
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for rel, content in files_map.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        ROOT, failures = root, []
        try:
            run_checks(tracked_files())
            return list(failures)
        finally:
            ROOT, failures = saved_root, saved_failures


def self_test():
    """Prove each check still rejects what it was written to reject.

    Reports explicitly rather than via assert: `python3 -O` strips assertions, and
    a self-test that silently passes under -O is the bug this file exists to catch.
    """
    problems = []

    def require(condition, message):
        if not condition:
            problems.append(message)

    def rejects(fixture, needle, message):
        require(any(needle in f for f in _run_fixture(fixture)), message)

    block, error = parse_frontmatter(SKILL.format(name="alpha"))
    require(error is None and "name: alpha" in block, "rejected valid frontmatter")
    for bad, kind in [("\n---\nname: x\n---\n", "not_at_start"),
                      ("<!-- leaked -->\n---\nname: x\n---\n", "not_at_start"),
                      ("---\nname: x\n", "unterminated"),
                      ("---\nname: x\n--- not a close\n", "unterminated"),
                      ("---\nname: x\n-----------\n", "unterminated")]:
        require(parse_frontmatter(bad) == (None, kind), f"frontmatter accepted {bad!r}")

    for line in ["", "<!-- x -->", "# heading", "Read the skill definition at ../SKILL.md"]:
        require(not WRAPPER_LINE1.match(line), f"wrapper line 1 accepted {line!r}")
    require(WRAPPER_LINE1.match(WRAPPER.format(name="a")).group(1) == "a", "line 1 target not captured")
    require(SKILL_REF.findall("see ../SKILL.md") == [], "SKILL_REF allows parent traversal")

    sentinel = "Bartholomew Quibblestein"
    try:
        yaml.safe_load(f'q: "{sentinel}: he said "yes" twice"\n')
        require(False, "malformed YAML fixture unexpectedly parsed")
    except yaml.YAMLError as exc:
        require(sentinel not in yaml_where(exc), "yaml_where leaks the source line")

    require(_run_fixture(_base_fixture()) == [], "clean fixture reported failures")

    rejects({**_base_fixture(), "alpha/SKILL.md": "<!-- x -->\n" + SKILL.format(name="alpha")},
            "must start at byte 0", "displaced frontmatter not caught")
    rejects({**_base_fixture(), "alpha/SKILL.md": SKILL.format(name="wrong")},
            "!= directory", "name/directory mismatch not caught")
    rejects({**_base_fixture(), "beta/SKILL.md": SKILL.format(name="beta"),
             "README.md": "| `/alpha` | Available |\n| `/beta` | Available |\n",
             "CLAUDE.md": "- `/alpha`\n- `/beta`\n"},
            "has no wrapper", "skill without a wrapper not caught")
    rejects({**_base_fixture(), ".claude/commands/alpha.md": WRAPPER.format(name="other")
             + "see alpha/SKILL.md\n", "other/SKILL.md": SKILL.format(name="other"),
             "README.md": "| `/alpha` | `/other` |\n", "CLAUDE.md": "- `/alpha` `/other`\n"},
            "line 1 runs", "mispointed wrapper line 1 not caught")
    rejects({**_base_fixture(), "README.md": "| `/alpha` | Coming soon |\n"},
            "marked 'coming soon'", "README table availability claim not caught")
    rejects({**_base_fixture(), "data/x.yml": 'a: "b "c" d"\n'},
            "does not parse", "unparseable YAML not caught")
    rejects({**_base_fixture(), "d/switches/s.yml": "interviewee: x\n"},
            "switch is missing top-level", "incomplete switch analysis not caught")
    rejects({**_base_fixture(), "d/switches/s.yml": "subject: x\njob_story: y\n"},
            "switch is missing top-level", "switch analysis without 'interviewee' not caught")
    rejects({**_base_fixture(),
             ".claude/commands/alpha.md": WRAPPER.format(name="alpha") + "see ghost/SKILL.md\n"},
            "which does not exist", "dangling SKILL.md reference not caught")
    rejects({**_base_fixture(), "alpha/SKILL.md": SKILL.format(name="alpha").rstrip("\n")},
            "missing trailing newline", "missing trailing newline not caught")
    rejects({**_base_fixture(), "CLAUDE.md": "nothing here\n"},
            "never lists it", "unadvertised skill not caught")

    require(_run_fixture({**_base_fixture(),
                          "CHANGELOG.md": "- `/alpha` is no longer marked coming soon.\n"}) == [],
            "changelog describing a past state was rejected")
    require(_run_fixture({**_base_fixture(),
                          "README.md": "`/alpha` is no longer coming soon.\n"}) == [],
            "past-tense prose in a non-exempt file was rejected")
    rejects({**_base_fixture(),
             "README.md": "| `/alpha` | Coming soon | docs no longer apply |\n"},
            "marked 'coming soon'", "neighbouring clause defused a live claim")
    require(_run_fixture({**_base_fixture(),
                          "TESTING.md": f"`/alpha` coming soon {ALLOW_MARKER}\n"}) == [],
            "explicit allow marker was ignored")

    if problems:
        print(f"self-test FAILED ({len(problems)}):")
        for line in problems:
            print(f"  - {line}")
        return 1
    print("self-test ok")
    return 0


def main():
    if "--self-test" in sys.argv:
        return self_test()

    files = tracked_files()
    if not files:
        fail("scripts/validate.py", "no files to validate")
    else:
        print("Validating jtbd skill collection...")
        read = run_checks(files)
        skills = len({f.split("/")[0] for f in skill_paths(files)})
        print(f"  {skills} skills, {len(read)} files inspected")

    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
