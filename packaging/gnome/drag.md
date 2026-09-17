# Moving the window on GNOME

The kitten is a frameless Qt window, so there is no title bar to grab.
GNOME/Mutter needs a compositor-native drag (`startSystemMove()`), which
kitten-pomo uses since **v0.2.0** — but a plain click also starts the
pomodoro at the same time, which can feel like the drag failed.

**How to move it:** press and **hold** the left mouse button on the kitten
(~250 ms), then drag. A quick click just starts the pomodoro (by design).

If a quick click-drag doesn't move it, use the hold-and-drag above. If it
still won't move, check that no GNOME extension is intercepting grabs and
file an issue with your GNOME/Mutter version.
