#!/usr/bin/env bash
# Desinstalador de Pixel Kitten Pomodoro.
# Por defecto CONSERVA tu historial pomodoro.jsonl. Usa --purge-data para borrarlo también.
set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/kitten-pomo"
BIN_LINK="$HOME/.local/bin/kitten-pomo"
DESKTOP_FILE="${XDG_DATA_HOME:-$HOME/.local/share}/applications/kitten-pomo.desktop"
PURGE=false
[ "${1:-}" = "--purge-data" ] && PURGE=true

if [ -L "$BIN_LINK" ] && [ "$(readlink "$BIN_LINK")" = "$DATA_DIR/kitten-pomo.py" ]; then
  rm "$BIN_LINK"
  echo "quitado: $BIN_LINK"
fi
rm -f "$DESKTOP_FILE" && echo "quitado: $DESKTOP_FILE"

if [ "$PURGE" = true ]; then
  rm -rf "$DATA_DIR" && echo "quitado (con datos): $DATA_DIR"
else
  if [ -f "$DATA_DIR/pomodoro.jsonl" ]; then
    find "$DATA_DIR" -mindepth 1 -maxdepth 1 ! -name 'pomodoro.jsonl' -exec rm -rf {} +
    echo "quitado código/assets, historial conservado en: $DATA_DIR/pomodoro.jsonl"
  else
    rm -rf "$DATA_DIR" && echo "quitado: $DATA_DIR"
  fi
fi

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "${XDG_DATA_HOME:-$HOME/.local/share}/applications" >/dev/null 2>&1 || true
fi
