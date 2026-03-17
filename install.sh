#!/bin/bash
set -e

SKILL_NAME="demo-creation"
INSTALL_DIR="$HOME/.snowflake/cortex/skills/$SKILL_NAME"

if [ -d "$INSTALL_DIR" ]; then
    echo "Skill '$SKILL_NAME' already exists at $INSTALL_DIR"
    read -p "Overwrite? (y/N): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Aborted."
        exit 0
    fi
    rm -rf "$INSTALL_DIR"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/demo-creation"

if [ ! -f "$SKILL_SRC/SKILL.md" ]; then
    echo "Error: Could not find demo-creation/SKILL.md relative to this script."
    echo "Make sure you run this from the repo root: ./install.sh"
    exit 1
fi

mkdir -p "$INSTALL_DIR"
cp -R "$SKILL_SRC/"* "$INSTALL_DIR/"

find "$INSTALL_DIR" -name ".venv" -type d -exec rm -rf {} + 2>/dev/null || true
find "$INSTALL_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$INSTALL_DIR" -name ".DS_Store" -delete 2>/dev/null || true

echo ""
echo "Installed '$SKILL_NAME' to $INSTALL_DIR"
echo ""
echo "Structure:"
find "$INSTALL_DIR" -type f | sed "s|$INSTALL_DIR/|  |" | sort
echo ""
echo "To use: open Cortex Code and type \$demo-creation or say 'create a demo for [account]'"
echo ""
echo "Dependencies (installed automatically via uv when the skill runs):"
echo "  - python-pptx"
echo "  - Pillow"
