# Pixel Kitten Pomodoro on GNOME

GNOME (Mutter) has no window-rule engine, so there is nothing to configure:

1. Run `./install.sh` (installs bin + `.desktop`).
2. Search "Pixel Kitten Pomodoro" in Activities and launch it.
3. Always-on-top is provided by the app itself (Qt `WindowStaysOnTopHint`
   → `_NET_WM_STATE_ABOVE`), no extensions needed.
4. Drag it wherever you want; position is manual.
5. Optional: add it to *Startup Applications* by copying the `.desktop`
   file to `~/.config/autostart/`.

Status: example **not tested** on stock GNOME. If something is off (focus,
position), open an issue with your GNOME version.
