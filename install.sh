#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="$SKILL_ROOT/project-manager-49"
mkdir -p "$SKILL_ROOT"
mkdir -p "$DEST_DIR"
cp -R "$SOURCE_DIR"/. "$DEST_DIR"/
printf 'Installed project-manager-49 to %s\n' "$DEST_DIR"
