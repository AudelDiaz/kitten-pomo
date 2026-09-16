#!/usr/bin/env bash
# Pixel Kitten Pomodoro uninstaller.
# By default it KEEPS your history (both the new XDG state log and any
# legacy log). Use --purge-data to remove those too.
set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/kitten-pomo"
STATE_LOG="${XDG_STATE_HOME:-$HOME/.local/state}/kitten-pomo/pomodoro.jsonl"
BIN_LINK="$HOME/.local/bin/kitten-pomo"
DESKTOP_FILE="${XDG_DATA_HOME:-$HOME/.local/share}/applications/kitten-pomo.desktop"
PURGE=false
[ "${1:-}" = "--purge-data" ] && PURGE=true

if command -v uv >/dev/null 2>&1 && uv tool list 2>/dev/null | grep -q '^kitten-pomo[ ,]'; then
  uv tool uninstall kitten-pomo
elif command -v pipx >/dev/null 2>&1 && pipx list --short 2>/dev/null | grep -q '^kitten-pomo[ ,]'; then
  pipx uninstall kitten-pomo
fi

# remove only symlinks we own (uv/pipx shims are already gone via tool uninstall)
if [ -L "$BIN_LINK" ]; then
  case "$(readlink "$BIN_LINK")" in
    "$DATA_DIR"/*) rm "$BIN_LINK" && echo "removed: $BIN_LINK" ;;
    *) echo "kept foreign file: $BIN_LINK" ;;
  esac
fi
rm -f "$DESKTOP_FILE" && echo "removed: $DESKTOP_FILE"

if [ "$PURGE" = true ]; then
  rm -rf "$DATA_DIR" && echo "removed (with staged files): $DATA_DIR"
  rm -f "$STATE_LOG" && echo "removed history: $STATE_LOG"
else
  if [ -f "$DATA_DIR/pomodoro.jsonl" ] || [ -f "$STATE_LOG" ]; then
    # drop code/assets, keep every history file where it is
    find "$DATA_DIR" -mindepth 1 -maxdepth 2 \
      ! -name 'pomodoro.jsonl' -exec rm -rf {} + 2>/dev/null || true
    echo "removed code/assets; history kept."
    [ -f "$DATA_DIR/pomodoro.jsonl" ] && echo "  $DATA_DIR/pomodoro.jsonl"
    [ -f "$STATE_LOG" ] && echo "  $STATE_LOG"
  else
    rm -rf "$DATA_DIR" && echo "removed: $DATA_DIR"
  fi
fi

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "${XDG_DATA_HOME:-$HOME/.local/share}/applications" >/dev/null 2>&1 || true
fi
