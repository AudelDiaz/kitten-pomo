#!/usr/bin/env bash
# Pixel Kitten Pomodoro installer.
#
# Preferred method: pipx (isolated venv, `kitten-pomo` lands on PATH).
# Fallback: plain copy install to XDG_DATA_HOME, same as before.
#   ./install.sh          # pipx if available, else copy
#   ./install.sh --copy   # force plain copy install
#
# Never touches window-manager config. History is never overwritten.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/kitten-pomo"
BIN_DIR="$HOME/.local/bin"
APPS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
BIN_LINK="$BIN_DIR/kitten-pomo"

MODE="auto"
[ "${1:-}" = "--copy" ] && MODE="copy"

install_desktop() { # $1 = icon path
  mkdir -p "$APPS_DIR"
  sed -e "s|@HOME@|$HOME|g" -e "s|@ICON@|$1|g" \
    "$REPO_DIR/packaging/kitten-pomo.desktop.in" \
    > "$APPS_DIR/kitten-pomo.desktop"
  if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
  fi
  if command -v desktop-file-validate >/dev/null 2>&1; then
    desktop-file-validate "$APPS_DIR/kitten-pomo.desktop"
  fi
}

free_bin_name() {
  # pipx refuses if something foreign owns the name; remove only our own symlink
  if [ -L "$BIN_LINK" ]; then
    case "$(readlink "$BIN_LINK")" in
      "$DATA_DIR"/*) rm "$BIN_LINK" ;;
    esac
  fi
}

if [ "$MODE" = "auto" ] && command -v pipx >/dev/null 2>&1; then
  echo "installing with pipx…"
  free_bin_name
  if pipx list --short 2>/dev/null | grep -q '^kitten-pomo[ ,]'; then
    pipx reinstall kitten-pomo
  else
    pipx install "$REPO_DIR"
  fi
  # stage the icon where the launcher expects it (venv paths are versioned)
  mkdir -p "$DATA_DIR/svg"
  cp "$REPO_DIR/src/kitten_pomo/assets/svg/kitten-idle.svg" "$DATA_DIR/svg/"
  install_desktop "$DATA_DIR/svg/kitten-idle.svg"
  echo "OK (pipx): run \`kitten-pomo\`"
else
  [ "$MODE" = "auto" ] && echo "pipx not found, plain copy install…"
  mkdir -p "$DATA_DIR" "$BIN_DIR"
  cp -r "$REPO_DIR/src/kitten_pomo" "$DATA_DIR/"
  chmod +x "$DATA_DIR/kitten_pomo/__main__.py"
  # drop the legacy flat layout from previous installs (history is kept)
  rm -f "$DATA_DIR/kitten-pomo.py" "$DATA_DIR/brain.py"
  rm -rf "$DATA_DIR/svg" "$DATA_DIR/sprites" "$DATA_DIR/sounds"
  ln -sfn "$DATA_DIR/kitten_pomo/__main__.py" "$BIN_LINK"
  install_desktop "$DATA_DIR/kitten_pomo/assets/svg/kitten-idle.svg"
  echo "OK (copy):"
  echo "  bin:      $BIN_LINK"
  echo "  data:     $DATA_DIR"
fi

echo "launcher: $APPS_DIR/kitten-pomo.desktop"
echo "Window rules: see packaging/niri|hyprland|gnome (not installed automatically)."
