#!/usr/bin/env bash
# Pixel Kitten Pomodoro installer.
#
# Order of preference:
#   1. uv tool install  (isolated venv, PySide6 included, `kitten-pomo` on PATH)
#   2. pipx install     (same idea, if you already have pipx and no uv)
#   3. plain copy       (no network/package manager needed, needs system PySide6)
#
#   ./install.sh          # auto: uv > pipx > copy
#   ./install.sh --copy   # force plain copy install
#
# If neither uv nor pipx exists, the script bootstraps user-local uv
# (https://astral.sh, ~/.local/bin, no sudo). Set ALLOW_UV_BOOTSTRAP=0
# to skip that and go straight to copy mode.
#
# Never touches window-manager config. History is never overwritten.
# Qt DBus app-id: the .desktop file carries StartupWMClass=kitten-pomo, so the
# system resolves the app-id via the .desktop. Do NOT call setDesktopFileName()
# in Python when a launcher is present — it causes a GNOME portal DBus crash.
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
  # uv/pipx refuse if something foreign owns the name; remove only our own symlink
  if [ -L "$BIN_LINK" ]; then
    case "$(readlink "$BIN_LINK")" in
      "$DATA_DIR"/*) rm "$BIN_LINK" ;;
    esac
  fi
}

ensure_uv() {
  command -v uv >/dev/null 2>&1 && return 0
  [ "${ALLOW_UV_BOOTSTRAP:-1}" = "0" ] && return 1
  command -v curl >/dev/null 2>&1 || return 1
  echo "uv not found, bootstrapping user-local uv (astral.sh, ~/.local/bin, no sudo)…"
  curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --quiet || return 1
  export PATH="$HOME/.local/bin:$PATH"
  command -v uv >/dev/null 2>&1
}

tool_installed() { # $1 = manager (uv|pipx)
  "$1" tool list 2>/dev/null | grep -q '^kitten-pomo[ ,]'
}

need_cmd() { # $1 = command, $2 = why
  command -v "$1" >/dev/null 2>&1 || {
    echo "error: '$1' not found ($2)" >&2
    return 1
  }
}

check_pyside() {
  # Copy installs run on the system interpreter, so PySide6 must be importable.
  # (uv/pipx installs bring their own isolated copy instead.)
  python3 -c "import PySide6, PySide6.QtSvg" 2>/dev/null || {
    cat >&2 <<'EOF'
error: Python 3 with PySide6 (incl. QtSvg) is required for a copy install.
Fix with ONE of:
  ./install.sh                       # retry: bootstraps uv and installs isolated
  pipx install /path/to/kitten-pomo  # same idea if you prefer pipx
  pip install --user PySide6         # distro permitting (PEP 668 may block it)
  sudo pacman -S python-pyside6  |  sudo apt install python3-pyside6  |  sudo dnf install python3-pyside6
EOF
    return 1
  }
}

if [ "$MODE" = "auto" ] && { command -v uv >/dev/null 2>&1 || ensure_uv; }; then
  echo "installing with uv tool…"
  free_bin_name
  if tool_installed uv; then
    uv tool upgrade kitten-pomo 2>/dev/null || uv tool install --force "$REPO_DIR"
  else
    uv tool install "$REPO_DIR"
  fi
  # stage the icon where the launcher expects it (venv paths are versioned)
  mkdir -p "$DATA_DIR/svg"
  cp "$REPO_DIR/src/kitten_pomo/assets/svg/kitten-idle.svg" "$DATA_DIR/svg/"
  install_desktop "$DATA_DIR/svg/kitten-idle.svg"
  echo "OK (uv tool): run \`kitten-pomo\`"
elif [ "$MODE" = "auto" ] && command -v pipx >/dev/null 2>&1; then
  echo "installing with pipx…"
  free_bin_name
  if tool_installed pipx; then
    pipx reinstall kitten-pomo
  else
    pipx install "$REPO_DIR"
  fi
  mkdir -p "$DATA_DIR/svg"
  cp "$REPO_DIR/src/kitten_pomo/assets/svg/kitten-idle.svg" "$DATA_DIR/svg/"
  install_desktop "$DATA_DIR/svg/kitten-idle.svg"
  echo "OK (pipx): run \`kitten-pomo\`"
else
  [ "$MODE" = "auto" ] && echo "no uv/pipx available, plain copy install…"
  need_cmd python3 "install Python 3 first" || exit 1
  check_pyside || exit 1
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
