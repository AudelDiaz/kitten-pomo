# Install paths

Two install flavors, same app. `install.sh` picks pipx when available
(`./install.sh --copy` forces the plain copy).

## pipx install (recommended)

| What     | Path                                              |
|----------|---------------------------------------------------|
| Code     | pipx venv (`~/.local/share/pipx/venvs/kitten-pomo`) |
| Binary   | `~/.local/bin/kitten-pomo` (console script)       |
| History  | `~/.local/state/kitten-pomo/pomodoro.jsonl`       |
| Launcher | `~/.local/share/applications/kitten-pomo.desktop` |

## Plain copy install (no pipx)

| What     | Path                                                        |
|----------|-------------------------------------------------------------|
| Code     | `~/.local/share/kitten-pomo/kitten_pomo/` (package + assets) |
| Binary   | `~/.local/bin/kitten-pomo` (symlink to `__main__.py`)       |
| History  | `~/.local/state/kitten-pomo/pomodoro.jsonl`                 |
| Launcher | `~/.local/share/applications/kitten-pomo.desktop`           |

History is never overwritten by the installer. On first run after upgrading
from a pre-`src/` install, an existing log at
`~/.local/share/kitten-pomo/pomodoro.jsonl` is copied once to the state dir.

The `.desktop` file is generated from `packaging/kitten-pomo.desktop.in`
by substituting `@HOME@` and `@ICON@`, so the repo contains no absolute
paths.
