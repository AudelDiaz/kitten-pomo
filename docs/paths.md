# Install paths

Three install flavors, same app. `install.sh` picks `uv`, then `pipx`,
then plain copy (`./install.sh --copy` forces the plain copy).

## uv tool install (recommended)

| What     | Path                                              |
|----------|---------------------------------------------------|
| Code     | uv tool venv (`~/.local/share/uv/tools/kitten-pomo`) |
| Binary   | `~/.local/bin/kitten-pomo` (+ `kitten-pomo-stats`) |
| History  | `~/.local/state/kitten-pomo/pomodoro.jsonl`       |
| Launcher | `~/.local/share/applications/kitten-pomo.desktop` |

## pipx install

Same layout as uv, with the venv at
`~/.local/share/pipx/venvs/kitten-pomo`.

## Plain copy install (no uv/pipx)

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
