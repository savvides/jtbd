#!/bin/bash
# jtbd installer — installs JTBD skills for Claude Code
# Usage: curl -sSL https://raw.githubusercontent.com/philippossavvides/jtbd/main/install.sh | bash

set -e

INSTALL_DIR="$HOME/.claude/skills/jtbd"
REPO_URL="https://github.com/philippossavvides/jtbd.git"
TAG="v1.0.0"

echo "jtbd installer"
echo "=============="
echo ""
echo "This will:"
echo "  1. Clone $REPO_URL (tag: $TAG)"
echo "  2. Install to $INSTALL_DIR"
echo ""

# Check prerequisites
if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git is required but not installed."
  exit 1
fi

# Check if already installed
if [ -d "$INSTALL_DIR" ]; then
  echo "jtbd is already installed at $INSTALL_DIR"
  echo ""
  echo "To update:"
  echo "  cd $INSTALL_DIR && git pull"
  echo ""
  echo "To reinstall:"
  echo "  rm -rf $INSTALL_DIR && bash install.sh"
  exit 0
fi

# Create parent directory
mkdir -p "$(dirname "$INSTALL_DIR")"

# Clone
echo "Cloning jtbd..."
git clone --branch "$TAG" --depth 1 "$REPO_URL" "$INSTALL_DIR" 2>/dev/null || \
  git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"

echo ""
echo "Installed to $INSTALL_DIR"
echo ""
echo "Try it: run /jtbd-switch in Claude Code"
echo "Docs:   $INSTALL_DIR/docs/methodology.md"
