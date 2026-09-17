#!/usr/bin/env bash
# Pixel Kitten Pomodoro installer (plain copy mode).
# Requires: python3 with PySide6 importable (sudo pacman -S python-pyside6 on Arch).
# History is never overwritten. No uv/pipx/pyproject needed.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/kitten-pomo"
BIN_DIR="$HOME/.local/bin"
APPS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
BIN_LINK="$BIN_DIR/kitten-pomo"

# check PySide6
python3 -c "import PySide6, PySide6.QtSvg" 2>/dev/null || {
  echo "error: Python 3 with PySide6 (incl. QtSvg) is required."
  echo "Fix: sudo pacman -S python-pyside6  |  sudo apt install python3-pyside6  |  sudo dnf install python3-pyside6"
  exit 1
}

mkdir -p "$DATA_DIR" "$BIN_DIR" "$APPS_DIR"

cp "$REPO_DIR/src/kitten_pomo/app.py" "$REPO_DIR/src/kitten_pomo/brain.py" "$DATA_DIR/"
chmod +x "$DATA_DIR/app.py"
cp -r "$REPO_DIR/src/kitten_pomo/assets" "$DATA_DIR/"

ln -sfn "$DATA_DIR/app.py" "$BIN_LINK"

sed "s|@HOME@|$HOME|g" "$REPO_DIR/packaging/kitten-pomo.desktop.in" \
  > "$APPS_DIR/kitten-pomo.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

echo "OK:"
echo "  bin:      $BIN_LINK"
echo "  data:     $DATA_DIR"
echo "  launcher: $APPS_DIR/kitten-pomo.desktop"
echo "Window rules: see packaging/niri|hyprland|gnome (not installed automatically)."
