#!/usr/bin/env python3
"""
Pixel Kitten Pomodoro — Option 2 POC (Python + niri Overlay via floating rule)
Left click → start 25:00 pomodoro | Right click → stop/reset
Stylish: translucent rounded card, Dracula palette, bob animation
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPoint, QSize, QByteArray, QRectF, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QFont, QCursor
from PySide6.QtSvg import QSvgRenderer

APP_ID = "kitten-pomo"

try:
    from kitten_pomo import brain as pomodoro_brain
except ImportError:
    try:
        import brain as pomodoro_brain
    except Exception as e:
        pomodoro_brain = None
        print(f"brain not loaded: {e}")


def _res_file(kind, filename):
    """Locate a bundled resource (svg|sprites|sounds) as a real Path.

    Works for pip/pipx installs (package data), fallback copy installs,
    repo checkouts (src layout) and the legacy flat layout.
    """
    here = Path(__file__).resolve().parent
    candidates = (
        here / "assets" / kind / filename,   # src layout / installed package
        here.parent / kind / filename,       # legacy flat layout
        here / kind / filename,              # legacy flat variant
    )
    for cand in candidates:
        if cand.exists():
            return cand
    return None


def _svg_bytes(name):
    # 1. package data (pip install / pipx) — works even from wheels
    try:
        from importlib import resources
        data = (resources.files("kitten_pomo") / "assets" / "svg" / f"{name}.svg").read_bytes()
        if data:
            return data
    except Exception:
        pass
    # 2. plain files (dev checkout, fallback install, legacy layout)
    p = _res_file("svg", f"{name}.svg")
    if p is not None:
        return p.read_bytes()
    return None


def svg_pixmap(name, size=96):
    """Render an SVG kitten to a crisp QPixmap at the given logical size."""
    data = _svg_bytes(name)
    if not data:
        return None
    renderer = QSvgRenderer(QByteArray(data))
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter, QRectF(0, 0, size, size))
    painter.end()
    return pix
POMO_MIN = 25
BREAK_MIN = 5

class KittenPomo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kitten-pomo")
        # Frameless + always-on-top. NOTE: no Qt.Tool — GNOME/Mutter centers
        # "utility" windows and won't let you drag them by their content.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)

        # state
        self.running = False
        self.paused = False
        self.on_break = False
        self.remaining = POMO_MIN * 60  # seconds
        self.drag_pos = None
        self.bob_y = 0
        self.bob_dir = 1

        # UI — 200x200 to fit 2-line status without clipping
        self.setFixedSize(200, 200)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14,14,14,14)
        layout.setSpacing(4)

        # zzz bubble — top-right of cat (child of main widget, not separate window)
        self.zzz_label = QLabel("z", self)
        self.zzz_label.setAlignment(Qt.AlignCenter)
        self.zzz_label.setStyleSheet("color: #f1fa8c; background: transparent;")
        self.zzz_label.setFont(QFont("JetBrainsMono Nerd Font", 11, QFont.Bold))
        self.zzz_label.setFixedSize(40, 20)
        self.zzz_label.move(102, 6)
        self.zzz_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.cat_label = QLabel()
        self.cat_label.setAlignment(Qt.AlignCenter)
        self.cat_label.setFixedSize(128,128)
        self.cat_label.setStyleSheet("background: transparent;")

        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("color: #f8f8f2; background: transparent;")
        self.timer_label.setFont(QFont("JetBrainsMono Nerd Font", 18, QFont.Bold))

        self.status_label = QLabel("Zzz click to start")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #bd93f9; background: transparent;")
        self.status_label.setFont(QFont("Sans", 8))
        self.status_label.setWordWrap(True)
        self.status_label.setFixedHeight(32)  # 2 lines

        layout.addWidget(self.cat_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.update_sprite("kitten-idle")
        self.update_timer_label()

        # timers
        self.tick_timer = QTimer(self)
        self.tick_timer.timeout.connect(self.tick)
        # smooth bob — sine wave, not step; disabled during focus for calm
        import math, time
        self._bob_t0 = time.time()
        self.bob_timer = QTimer(self)
        self.bob_timer.timeout.connect(self.bob)
        self.bob_timer.start(40)  # 25fps smooth

        # zzz animation — cycles z → zz → zzz when idle
        self.zzz_step = 0
        self.zzz_timer = QTimer(self)
        self.zzz_timer.timeout.connect(self.animate_zzz)
        self.zzz_timer.start(520)
        self.update_zzz_visibility()

        # kill confirm — middle click twice within 3s
        self._pending_kill = False
        self._kill_timer = QTimer(self)
        self._kill_timer.setSingleShot(True)
        self._kill_timer.timeout.connect(self._cancel_kill_confirm)

        # allow dragging
        self.setMouseTracking(True)

    def update_sprite(self, name):
        # render SVG at exactly the cat_label's box size for crisp scaling
        disp = self.cat_label.size() or QSize(128, 128)
        pix = svg_pixmap(name, disp.width())
        if pix is not None:
            self.cat_label.setPixmap(pix)
        else:
            # fallback to old PNG sprites
            p = _res_file("sprites", f"{name}.png")
            if p is not None:
                self.cat_label.setPixmap(QPixmap(str(p)).scaled(disp, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.cat_label.setText("ฅ^•ﻌ•^ฅ")

    def update_timer_label(self):
        m, s = divmod(self.remaining, 60)
        self.timer_label.setText(f"{m:02d}:{s:02d}")

    def paintEvent(self, event):
        # original dark glass — 80% opacity, 190x190
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(self.rect().adjusted(2,2,-2,-2), 18, 18)
        p.fillPath(path, QColor(40,42,54, 204))  # #282a36 80% (204/255)
        p.setPen(QColor(189,147,249, 60))
        p.drawPath(path)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            # when expanded for break, click collapses the big bubble
            if getattr(self, "_expanded", False) and self.on_break:
                self.collapse_from_break()
                self.reset_pomo()
                e.accept()
                return
            # Shift+Left = simulate completion (for testing, no 25min wait)
            if e.modifiers() & Qt.ShiftModifier:
                self.simulate_completion()
                e.accept()
                return
            # left click → start (only when idle)
            if not self.running and not self.paused:
                self.start_pomo()
            e.accept()
        elif e.button() == Qt.RightButton:
            # Shift+Right = also simulate (alternative)
            if e.modifiers() & Qt.ShiftModifier:
                self.simulate_completion()
                e.accept()
                return
            self.reset_pomo()
            e.accept()
        elif e.button() == Qt.MiddleButton:
            # center click → confirm kill (needs second click within 3s)
            if not self._pending_kill:
                self._pending_kill = True
                self._kill_timer.start(3000)
                # save current status to restore if cancelled
                self._prev_status_text = self.status_label.text()
                self._prev_status_style = self.status_label.styleSheet()
                self.status_label.setText("Middle click again\n to kill (3s)")
                self.status_label.setStyleSheet("color: #ffb86c; background: transparent;")
                self.notify("Confirm kill", "Middle click again within 3s to close kitten")
            else:
                self._kill_timer.stop()
                self.notify("Kitten bye", "Purr — see you next pomodoro!")
                QApplication.quit()
            e.accept()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton and self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)
            e.accept()

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton:
            # double click → pause / resume
            if self.running and not self.paused:
                self.pause_pomo()
            elif self.paused:
                self.resume_pomo()
            e.accept()
        else:
            super().mouseDoubleClickEvent(e)

    def _cancel_kill_confirm(self):
        self._pending_kill = False
        # restore status (idle vs running vs paused) — 2-line friendly
        if self.running and not self.paused:
            self.status_label.setText("● focus\n double click to pause")
            self.status_label.setStyleSheet("color: #ff5555; background: transparent;")
        elif self.paused:
            self.status_label.setText("⏸ paused\n double click to resume")
            self.status_label.setStyleSheet("color: #f1fa8c; background: transparent;")
        else:
            self.status_label.setText("Zzz click to start")
            self.status_label.setStyleSheet("color: #bd93f9; background: transparent;")

    def keyPressEvent(self, e):
        # T = simulate pomodoro completion instantly (cozy test)
        if e.key() in (Qt.Key_T, Qt.Key_T | 0x20):  # T/t
            self.simulate_completion()
            e.accept()
        elif e.key() == Qt.Key_Escape and self._pending_kill:
            self._cancel_kill_confirm()
            e.accept()
        else:
            super().keyPressEvent(e)

    def mouseReleaseEvent(self, e):
        self.drag_pos = None

    def update_zzz_visibility(self):
        # zzz only when idle (not running) — black cat sleeping
        is_idle = not self.running
        self.zzz_label.setVisible(is_idle)
        self.zzz_label.raise_()

    def animate_zzz(self):
        if self.running:
            return
        self.zzz_step = (self.zzz_step + 1) % 3
        texts = ["z", "zz", "zzz"]
        self.zzz_label.setText(texts[self.zzz_step])
        # gentle float for bubble
        self.zzz_label.move(102, 6 + (self.zzz_step * 1))

    def pause_pomo(self):
        if not self.running or self.paused: return
        self.tick_timer.stop()
        self.paused = True
        self.status_label.setText("⏸ paused\n double click to resume")
        self.status_label.setStyleSheet("color: #f1fa8c; background: transparent;")
        self.notify("Paused", "Double click to resume")

    def resume_pomo(self):
        if not self.paused: return
        self.paused = False
        self.status_label.setText("● focus\n double click to pause")
        self.status_label.setStyleSheet("color: #ff5555; background: transparent;")
        self.tick_timer.start(1000)
        self.notify("Resumed", "Back to focus!")

    def start_pomo(self):
        if self.running: return
        self.running = True
        self.paused = False
        self.on_break = False
        self.remaining = POMO_MIN * 60
        self.update_sprite("kitten-work")  # black + yellow open eyes
        self.update_zzz_visibility()  # hide zzz
        self.status_label.setText("● focus\n double click to pause")
        self.status_label.setStyleSheet("color: #ff5555; background: transparent;")
        self.tick_timer.start(1000)
        # optional: notify via noctalia if available
        self.notify("Kitten Pomodoro started", f"{POMO_MIN} min focus — you got this!")

    def reset_pomo(self):
        self.tick_timer.stop()
        self.running = False
        self.paused = False
        self.on_break = False
        self.remaining = POMO_MIN * 60
        self.update_timer_label()
        self.update_sprite("kitten-idle")  # black + closed eyes
        self.update_zzz_visibility()  # show zzz again
        self.status_label.setText("Zzz click to start")
        self.status_label.setStyleSheet("color: #bd93f9; background: transparent;")
        if pomodoro_brain:
            try: pomodoro_brain.log_reset()
            except: pass
        self.notify("Reset", "25:00 ready")

    def simulate_completion(self):
        """Instant test: pretend 25min just finished, trigger cozy break without waiting."""
        if self.running and not self.paused:
            self.remaining = 2
            self.update_timer_label()
            self.notify("Simulating…", "2 sec to cozy break!")
        elif not self.running:
            # start then instantly near end
            self.start_pomo()
            self.remaining = 3
            self.update_timer_label()

    def play_cozy_sound(self):
        import subprocess, shutil
        # prefer paplay / aplay with our wav, fallback to mpv, fallback to notify
        bell = _res_file("sounds", "bell.wav")
        purr = _res_file("sounds", "purr.wav")
        # try paplay (PulseAudio), then aplay, then mpv, then ffplay
        sounds = [s for s in (bell, purr) if s is not None]
        if sounds:
            bell_file = str(sounds[0])
            for cmd in [["paplay", bell_file], ["aplay", bell_file], ["mpv", "--no-video", bell_file], ["ffplay", "-nodisp", "-autoexit", bell_file]]:
                if shutil.which(cmd[0]):
                    try:
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        return
                    except: pass
        # fallback: try purr explicitly
        if purr is not None:
            for cmd in [["paplay", str(purr)], ["aplay", str(purr)]]:
                if shutil.which(cmd[0]):
                    try:
                        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        return
                    except: pass

    def shake(self):
        # 5s cozy wobble — whole bubble, long and soft
        orig = self.pos()
        self._shake_step = 0
        # 25 steps, 200ms each = 5000ms, decaying
        offsets = [-16, 16, -15, 15, -14, 14, -12, 12, -10, 10, -8, 8, -6, 6, -5, 5, -4, 4, -3, 3, -2, 2, -1, 1, 0]
        def do_shake():
            if self._shake_step < len(offsets):
                self.move(orig + QPoint(offsets[self._shake_step], 0))
                if self._shake_step % 2 == 0:
                    self.timer_label.setStyleSheet("color: #ff5555; background: transparent;")
                else:
                    self.timer_label.setStyleSheet("color: #f8f8f2; background: transparent;")
                self._shake_step += 1
                QTimer.singleShot(200, do_shake)
            else:
                self.move(orig)
                self.timer_label.setStyleSheet("color: #f8f8f2; background: transparent;")
        do_shake()
        self._shake_chain = do_shake

    def expand_for_break(self):
        # pop disabled per user — keep 200x200, no expand
        return

    def collapse_from_break(self):
        return

    def tick(self):
        if not self.running or self.paused: return
        self.remaining -= 1
        self.update_timer_label()
        if self.remaining <= 0:
            self.tick_timer.stop()
            self.running = False
            if not self.on_break:
                # work finished → log + decide long break (20) if 4 in 150min
                if pomodoro_brain:
                    try: pomodoro_brain.log_work_completed(POMO_MIN)
                    except: pass
                    try: next_break = pomodoro_brain.next_break_minutes(150)
                    except: next_break = BREAK_MIN
                else:
                    next_break = BREAK_MIN
                self._current_break = next_break
                self.play_cozy_sound()
                self.shake()
                self.on_break = True
                self.paused = False
                self.remaining = next_break * 60
                self.update_sprite("kitten-break")
                if next_break == 20:
                    self.status_label.setText(f"✓ 4 done! long break {next_break}:00\n cozy stretch!")
                else:
                    self.status_label.setText(f"✓ break {next_break}:00\n cozy break!")
                self.status_label.setStyleSheet("color: #50fa7b; background: transparent;")
                self.notify("Purr! Pomodoro done", f"Take {next_break} min break 💤")
                self.update_timer_label()
                QTimer.singleShot(900, self.start_break_countdown)
            else:
                # break finished → log break + back to idle
                if pomodoro_brain:
                    try: pomodoro_brain.log_break_completed(getattr(self, "_current_break", BREAK_MIN))
                    except: pass
                self.on_break = False
                self.paused = False
                self.play_cozy_sound()
                self.shake()
                self.update_sprite("kitten-idle")
                self.remaining = POMO_MIN * 60
                self.update_timer_label()
                self.status_label.setText("✓ break over\n Zzz click to start")
                self.status_label.setStyleSheet("color: #bd93f9; background: transparent;")
                self.update_zzz_visibility()
                self.notify("Break over", "Ready for next pomodoro?")

    def start_break_countdown(self):
        if self.on_break and not self.running:
            self.running = True
            self.paused = False
            self.tick_timer.start(1000)
            self.status_label.setText(f"☕ break\n {BREAK_MIN:02d}:00")
            self.update_zzz_visibility()

    def bob(self):
        import math, time
        t = time.time() - self._bob_t0
        # all states breathe smoothly — same soft sine as sleeping
        if not self.running and not self.paused:
            amp, freq = 1.6, 0.75  # idle sleeping (what you liked)
        elif self.running and not self.on_break:
            amp, freq = 1.4, 0.68  # focus — same smoothness, just a touch calmer
        else:
            amp, freq = 1.3, 0.62  # break / paused — softest
        dy = math.sin(t * freq * 2 * math.pi) * amp
        self.cat_label.move(self.cat_label.x(), int(10 + dy))

    def notify(self, title, body):
        # try noctalia, fallback to notify-send
        import subprocess, shutil
        if shutil.which("noctalia"):
            subprocess.Popen(["noctalia","msg","notification-show", title, body],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif shutil.which("notify-send"):
            subprocess.Popen(["notify-send", title, body],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    """Entry point for the `kitten-pomo` console script."""
    app = QApplication(sys.argv)
    # set app id for niri window-rule matching
    app.setDesktopFileName(APP_ID)
    w = KittenPomo()
    # start near bottom-right; niri will also apply default-floating-position via rule
    screen = app.primaryScreen().geometry()
    w.move(screen.width() - 200, screen.height() - 260)
    w.show()
    # GNOME/Mutter re-centers utility-ish windows after mapping; re-assert our
    # position once the window is actually on screen (no-op on niri).
    QTimer.singleShot(120, lambda: w.move(screen.width() - 200, screen.height() - 260))
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
