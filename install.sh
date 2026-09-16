#!/usr/bin/env bash
# Pixel Kitten Pomodoro installer.
# Copies code + assets to XDG_DATA_HOME (~/.local/share/kitten-pomo),
# creates the ~/.local/bin symlink and installs the .desktop launcher.
# Never touches your niri/hyprland/GNOME config or your existing pomodoro.jsonl.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/kitten-pomo"
BIN_DIR="$HOME/.local/bin"
APPS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

mkdir -p "$DATA_DIR" "$BIN_DIR" "$APPS_DIR"

cp "$REPO_DIR/kitten-pomo.py" "$REPO_DIR/brain.py" "$DATA_DIR/"
chmod +x "$DATA_DIR/kitten-pomo.py"
cp -r "$REPO_DIR/assets/svg" "$REPO_DIR/assets/sprites" "$REPO_DIR/assets/sounds" "$DATA_DIR/"

# History is never overwritten: the installer copies no *.jsonl files.
if [ ! -e "$DATA_DIR/pomodoro.jsonl" ]; then
  echo "(no previous history, it will be created when you complete your first pomodoro)"
fi

ln -sfn "$DATA_DIR/kitten-pomo.py" "$BIN_DIR/kitten-pomo"

sed "s|@HOME@|$HOME|g" "$REPO_DIR/packaging/kitten-pomo.desktop.in" \
  > "$APPS_DIR/kitten-pomo.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

if command -v desktop-file-validate >/dev/null 2>&1; then
  desktop-file-validate "$APPS_DIR/kitten-pomo.desktop"
fi

echo "OK:"
echo "  bin:      $BIN_DIR/kitten-pomo"
echo "  data:     $DATA_DIR"
echo "  launcher: $APPS_DIR/kitten-pomo.desktop"
echo "Window rules: see packaging/niri|hyprland|gnome (not installed automatically)."
