#!/usr/bin/env bash
set -euo pipefail

# Generate HTML API docs for the Python source in src/
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="$REPO_ROOT/docs/api"
SRC_DIR="$REPO_ROOT/src"

PDOC_CMD="pdoc"
if ! command -v "$PDOC_CMD" >/dev/null 2>&1; then
  PDOC_CMD="python3 -m pdoc"
fi

mkdir -p "$OUT_DIR"

# pdoc v16+: use -o to write HTML into OUT_DIR
bash -lc "$PDOC_CMD -o \"$OUT_DIR\" \"$SRC_DIR\""

# pdoc nests output inside a folder named after the package; flatten entrypoint index to docs/api/index.html if present
PACKAGE_INDEX="$OUT_DIR/src/index.html"
if [ -f "$PACKAGE_INDEX" ]; then
  cp "$PACKAGE_INDEX" "$OUT_DIR/index.html"
fi

echo "API docs generated to $OUT_DIR"