# Install paths

`install.sh` honors `XDG_DATA_HOME` (default `~/.local`):

| What     | Path                                               |
|----------|----------------------------------------------------|
| Code     | `~/.local/share/kitten-pomo/{kitten-pomo.py,brain.py}` |
| Assets   | `~/.local/share/kitten-pomo/{svg,sprites,sounds}/` |
| History  | `~/.local/share/kitten-pomo/pomodoro.jsonl` (the installer **never** touches it) |
| Binary   | `~/.local/bin/kitten-pomo` (symlink)               |
| Launcher | `~/.local/share/applications/kitten-pomo.desktop`  |

The `.desktop` file is generated from `packaging/kitten-pomo.desktop.in`
by substituting `@HOME@` with your `$HOME`, so the repo contains no
absolute paths.
