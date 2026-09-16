# Pixel Kitten Pomodoro 🐈‍⬛

A black pixel-art kitten that floats on your desktop and keeps you company
through your pomodoros. Cozy, not strict: it invites you to take a break,
never blocks you.

## Controls

| Action              | Effect                        |
|---------------------|-------------------------------|
| Left click          | Start a 25:00 pomodoro        |
| Double click        | Pause / resume                |
| Right click         | Reset (breaks the streak)     |
| Wheel (2x in 3s)    | Quit (with confirmation)      |
| `Shift+Click` or `T`| Simulate finish (2s, for testing) |
| Drag                | Move                          |

On completion: cozy sound + 5s shake + 5:00 break inside the bubble.
**4 pomodoros in a row within 150 min → 20:00 long break.**

## Install

Requires Python 3 + PySide6 (`pip install PySide6`).

```bash
./install.sh
# or: make install
```

Installs to `~/.local/share/kitten-pomo`, symlinks `~/.local/bin/kitten-pomo`,
and installs the `.desktop` launcher. Your existing `pomodoro.jsonl` is
always preserved. See `docs/paths.md`.

```bash
./uninstall.sh               # keeps history
./uninstall.sh --purge-data  # removes everything including history
```

## Window rules per environment

| Niri | Hyprland | GNOME |
|------|----------|-------|
| ✅ tested | 🧪 contrib | 🧪 contrib |

See `docs/compositors.md` and `packaging/`.

## History

Every cycle is logged to `pomodoro.jsonl` (`ts/type/duration/completed`).
Example at `examples/pomodoro.sample.jsonl`.

```bash
python3 brain.py --stats   # current streak and next break
```

Share the log with your AI agent/Harness to analyze focus peaks and streaks.

## License

MIT — see `LICENSE`.
