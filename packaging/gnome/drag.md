# Moving the window on GNOME

The kitten is a frameless Qt window, so there is no title bar to grab.
Two ways to move it:

**Option A — Super + drag (recommended):** hold the Super (Windows) key and
drag anywhere on the window. This is Mutter's native move, works on any
frameless window, and doesn't conflict with the pomodoro click.

**Option B — hold-and-drag:** press and **hold** the left mouse button on
the kitten (~250 ms), then drag. A quick click just starts the pomodoro
(by design). This uses the compositor-native `startSystemMove()` since
v0.2.0.

If neither works, check that no GNOME extension is intercepting grabs and
file an issue with your GNOME/Mutter version.
