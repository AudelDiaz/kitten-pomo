# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- GNOME: window no longer closes on launch (removed `setDesktopFileName` which caused a portal DBus app-id conflict)
- GNOME: removed periodic `setWindowFlags` timer that caused flicker/close
- GNOME: restored `Qt.Tool` window flag (keeps window out of taskbar/dock)

### Changed
- Installer prefers `uv tool install` (with bootstrap), then `pipx`, then plain copy
- README updated with GNOME-specific install + drag instructions

## [0.2.0] - 2026-09-17

### Added
- `pyproject.toml` with `uv tool install` / `pipx install` / plain copy fallback
- `kitten-pomo-stats` console script (streak + next break)
- History in XDG state (`~/.local/state/kitten-pomo/`) with one-time migration from legacy installs
- `install.sh` preflight: checks python3 + PySide6 before copy install
- `uninstall.sh` handles uv/pipx tools and keeps history by default
- GNOME drag support via compositor-native `startSystemMove()` with manual fallback
- `packaging/gnome/drag.md` documenting hold-and-drag on GNOME
- Screenshots of all 4 states in `docs/screenshots/`

### Changed
- Dropped `Qt.Tool` window flag (GNOME/Mutter centers utility windows and blocks content-drag)
- Position re-asserted 120ms after window map (GNOME centering workaround)
- README rewritten in casual English, neutral wording ("the kitten")
- All code, comments, docs and README in English

### Fixed
- GNOME: window no longer centered, draggable via hold-and-drag
- `__main__.py` shebang + `sys.path` bootstrap for symlink execution
- `chmod +x` on `__main__.py` in copy installs

## [0.1.0] - 2026-09-16

### Added
- Initial public release
- Floating black pixel-kitten Pomodoro (PySide6): 25:00 focus, 5:00 cozy break, 20:00 long break after 4 in a row (150-min window)
- Cozy finish: sound + 5s shake + in-bubble countdown, never fullscreen-blocking
- `brain.py` streak log in XDG state with one-time migration
- `install.sh` / `uninstall.sh` (XDG-aware, history always preserved)
- Niri window rule (tested), Hyprland + GNOME examples (contrib)
- SVG pixel-cat skins (crisp at any size) + PNG fallbacks + sounds
- MIT license
