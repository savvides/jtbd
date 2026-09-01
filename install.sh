#!/bin/bash
# jtbd installer
#
# Open source Jobs to Be Done skills for Antigravity, Gemini, and Claude Code.

cat <<'EOF'
jtbd supports Google Antigravity, Gemini, and Claude Code:

1. For Google Antigravity & Gemini:
   git clone https://github.com/savvides/jtbd.git ~/.gemini/config/plugins/jtbd

2. For Claude Code:
   Run inside Claude Code:
     /plugin marketplace add savvides/jtbd
     /plugin install jtbd@jtbd
   Then restart Claude Code or run /reload-plugins.

Docs: https://github.com/savvides/jtbd
EOF

