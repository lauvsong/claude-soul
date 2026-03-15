#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Installing claude-soul → $CLAUDE_DIR"

# Backup existing settings
if [ -d "$CLAUDE_DIR" ]; then
  echo "Backing up existing ~/.claude → ~/.claude.bak"
  cp -r "$CLAUDE_DIR" "$CLAUDE_DIR.bak" 2>/dev/null || true
fi

mkdir -p "$CLAUDE_DIR"

# Copy files
for item in CLAUDE.md settings.json; do
  cp "$REPO_DIR/$item" "$CLAUDE_DIR/"
done

for dir in rules hooks skills scheduled-tasks; do
  cp -r "$REPO_DIR/$dir" "$CLAUDE_DIR/"
done

echo ""
echo "Done! Installed:"
echo "  CLAUDE.md, settings.json, rules/, hooks/, skills/, scheduled-tasks/"
echo ""
echo "Note: settings.json의 env 섹션(토큰 등)과 플러그인은 직접 추가하세요."
