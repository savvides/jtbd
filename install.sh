#!/bin/bash
# jtbd installer — installs JTBD skills for Claude Code
# Usage: curl -sSL https://raw.githubusercontent.com/savvides/jtbd/main/install.sh | bash

set -e

INSTALL_DIR="$HOME/.claude/skills/jtbd"
REPO_URL="https://github.com/savvides/jtbd.git"
# No releases are tagged yet, so install tracks main. Set JTBD_TAG to pin one.
TAG="${JTBD_TAG:-}"

echo "jtbd installer"
echo "=============="
echo ""
echo "This will:"
if [ -n "$TAG" ]; then
  echo "  1. Clone $REPO_URL (tag: $TAG)"
else
  echo "  1. Clone $REPO_URL (latest from main)"
fi
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
if [ -n "$TAG" ]; then
  git clone --branch "$TAG" --depth 1 "$REPO_URL" "$INSTALL_DIR" 2>/dev/null || {
    echo "  tag $TAG not found, installing latest from main"
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
  }
else
  git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi

echo ""
echo "Installed to $INSTALL_DIR"
echo ""
echo "Try it: run /jtbd-switch in Claude Code"
echo "Docs:   $INSTALL_DIR/docs/methodology.md"
