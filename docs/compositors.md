# Window rules per environment

Always-on-top is provided by the app itself (Qt `WindowStaysOnTopHint`).
The rules below only fine-tune size, position, and opacity.

| Environment | Status     | File                                |
|-------------|------------|-------------------------------------|
| Niri        | ✅ tested  | `packaging/niri/kitten-pomo.kdl`    |
| Hyprland    | 🧪 contrib | `packaging/hyprland/kitten-pomo.conf` |
| GNOME       | 🧪 contrib | `packaging/gnome/README.md` (no rules) |

## Niri

Paste `packaging/niri/kitten-pomo.kdl` into your rules file and reload Niri.
200x200 window, bottom-right, no initial focus, 0.8 opacity.

## Hyprland

Add `source = ~/path/to/kitten-pomo/packaging/hyprland/kitten-pomo.conf`
to your `hyprland.conf`. Example not tested by the author; PRs with a
screenshot are welcome.

## GNOME

No rules: launch it from the app grid and drag the window where you want it.
See `packaging/gnome/README.md` for autostart.
