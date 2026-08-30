#!/bin/bash
# jtbd installer
#
# Kept for people who land here from an old link. The supported install is the
# Claude Code plugin marketplace, which is two commands inside Claude Code and
# gives you versioned installs, updates and a clean uninstall:
#
#   /plugin marketplace add savvides/jtbd
#   /plugin install jtbd@jtbd
#
# Cloning this repo into ~/.claude/skills/ does NOT register the skills. Claude
# Code discovers personal skills at ~/.claude/skills/<skill-name>/SKILL.md, one
# level deep, and a clone puts them two levels deep. That is what this script
# used to do, and why it is no longer the install path.

cat <<'EOF'
jtbd is installed as a Claude Code plugin.

Run these two commands inside Claude Code:

  /plugin marketplace add savvides/jtbd
  /plugin install jtbd@jtbd

Then restart Claude Code, or run /reload-plugins, and /jtbd-demo will be available.

Docs: https://github.com/savvides/jtbd
EOF
