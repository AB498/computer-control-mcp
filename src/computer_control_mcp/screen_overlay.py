"""On-screen activity indicator for computer-control actions.

The overlay is intentionally implemented with Tkinter so the MCP keeps its
existing dependency set.  It uses a transparent, click-through Windows window:
the desktop remains usable while the green border and status card are visible.
"""

from __future__ import annotations

import atexit
import ctypes
import os
import queue
import re
import sys
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator, Optional


_ENABLE_ENV = "COMPUTER_CONTROL_MCP_OVERLAY"
_TEXT_ENV = "COMPUTER_CONTROL_MCP_OVERLAY_TEXT"
_TRANSPARENT_COLOR = "#010203"
_GREEN = "#22C55E"
_PANEL_BG = "#0B1220"
_TEXT = "#F0FDF4"
_MUTED_TEXT = "#A7F3D0"


def _overlay_enabled() -> bool:
    """Return whether the platform and configuration support the overlay."""
    if sys.platform != "win32":
        return False
    setting = os.getenv(_ENABLE_ENV, "1").strip().lower()
    return setting not in {"0", "false", "off", "no"}


def _safe_label(value: str, limit: int = 96) -> str:
    """Keep overlay text on a single line and reasonably short."""
    compact = re.sub(r"\s+", " ", str(value)).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1] + "…"


def _log_overlay_error(message: str) -> None:
    """Log without writing to stdout, which is reserved for MCP JSON-RPC."""
    try:
        print(f"[COMPUTER_CONTROL_MCP overlay] {message}", file=sys.stderr)
    except Exception:
        pass


@dataclass(frozen=True)
class _ShowCommand:
    token: int
    action: str
    detail: str


@dataclass(frozen=True)
class _HideCommand:
    token: Optional[int]
    delay: float
    done: Optional[threading.Event] = None


@dataclass(frozen=True)
class _StopCommand:
    done: threading.Event


class _OverlayWindow(threading.Thread):
    """Own a Tk event loop in a daemon thread."""

    def __init__(self) -> None:
        super().__init__(name="computer-control-overlay", daemon=True)
        self.commands: queue.Queue[object] = queue.Queue()
        self.ready = threading.Event()
        self.failed = False
        self.root = None
        self.window = None
        self.hwnd = None
        self.canvas = None
        self.title_label = None
        self.action_label = None
        self.detail_label = None
        self._current_token: Optional[int] = None
        self._hide_after_id = None

    def run(self) -> None:
        try:
            self._attach_to_default_desktop()
            self._create_window()
        except Exception as exc:
            self.failed = True
            _log_overlay_error(f"could not create activity overlay: {exc}")
            self.ready.set()
            return

        self.ready.set()
        try:
            self.root.after(20, self._drain_commands)
            self.root.mainloop()
        except Exception as exc:
            self.failed = True
            _log_overlay_error(f"overlay event loop stopped: {exc}")

    @staticmethod
    def _attach_to_default_desktop() -> None:
        """Create the overlay on the interactive Windows desktop when possible."""
        try:
            user32 = ctypes.windll.user32
            desktop = user32.OpenDesktopW("Default", 0, False, 0x01FF)
            if desktop:
                try:
                    user32.SetThreadDesktop(desktop)
                finally:
                    user32.CloseDesktop(desktop)
        except Exception:
            # The normal process desktop is still a valid fallback.
            pass

    def _create_window(self) -> None:
        import tkinter as tk

        user32 = ctypes.windll.user32
        left = user32.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
        top = user32.GetSystemMetrics(77)  # SM_YVIRTUALSCREEN
        width = user32.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
        height = user32.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN
        if width <= 0 or height <= 0:
            raise RuntimeError("Windows returned invalid virtual-screen dimensions")

        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("Computer Control MCP Activity")

        self.window = tk.Toplevel(self.root)
        self.window.withdraw()
        self.window.overrideredirect(True)
        self.window.configure(bg=_TRANSPARENT_COLOR)
        self.window.geometry(f"{width}x{height}{left:+d}{top:+d}")
        self.window.attributes("-topmost", True)
        self.window.attributes("-transparentcolor", _TRANSPARENT_COLOR)

        self.canvas = tk.Canvas(
            self.window,
            bg=_TRANSPARENT_COLOR,
            highlightthickness=0,
            borderwidth=0,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(
            3,
            3,
            width - 3,
            height - 3,
            outline=_GREEN,
            width=6,
        )

        card = tk.Frame(
            self.window,
            bg=_PANEL_BG,
            highlightbackground=_GREEN,
            highlightcolor=_GREEN,
            highlightthickness=2,
            padx=16,
            pady=10,
        )
        card.place(relx=1.0, rely=1.0, x=-22, y=-22, anchor="se")

        brand_font = ("Consolas", 8, "bold")
        action_font = ("Microsoft YaHei UI", 12, "bold")
        detail_font = ("Microsoft YaHei UI", 9)

        tk.Label(
            card,
            text="COMPUTER CONTROL MCP",
            bg=_PANEL_BG,
            fg=_GREEN,
            font=brand_font,
            anchor="w",
        ).pack(fill="x")
        self.title_label = tk.Label(
            card,
            text=os.getenv(_TEXT_ENV, "AI is controlling the computer"),
            bg=_PANEL_BG,
            fg=_TEXT,
            font=action_font,
            anchor="w",
        )
        self.title_label.pack(fill="x", pady=(2, 0))
        self.action_label = tk.Label(
            card,
            text="",
            bg=_PANEL_BG,
            fg=_MUTED_TEXT,
            font=detail_font,
            anchor="w",
            justify="left",
        )
        self.action_label.pack(fill="x", pady=(3, 0))
        self.detail_label = tk.Label(
            card,
            text="",
            bg=_PANEL_BG,
            fg="#94A3B8",
            font=detail_font,
            anchor="w",
            justify="left",
        )
        self.detail_label.pack(fill="x")

        self.window.update_idletasks()
        child_hwnd = self.window.winfo_id()
        self.hwnd = user32.GetParent(child_hwnd) or child_hwnd
        self._make_click_through()

    def _make_click_through(self) -> None:
        """Apply Windows extended styles so the overlay cannot intercept input."""
        user32 = ctypes.windll.user32
        hwnd = self.hwnd or self.window.winfo_id()
        gwl_exstyle = -20
        ws_ex_layered = 0x00080000
        ws_ex_transparent = 0x00000020
        ws_ex_toolwindow = 0x00000080
        ws_ex_noactivate = 0x08000000

        get_style = getattr(user32, "GetWindowLongPtrW", user32.GetWindowLongW)
        set_style = getattr(user32, "SetWindowLongPtrW", user32.SetWindowLongW)
        get_style.argtypes = [ctypes.c_void_p, ctypes.c_int]
        get_style.restype = ctypes.c_longlong
        set_style.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_longlong]
        set_style.restype = ctypes.c_longlong
        style = get_style(hwnd, gwl_exstyle)
        style |= (
            ws_ex_layered
            | ws_ex_transparent
            | ws_ex_toolwindow
            | ws_ex_noactivate
        )
        set_style(hwnd, gwl_exstyle, style)

    def _show(self, command: _ShowCommand) -> None:
        self._cancel_scheduled_hide()
        self._current_token = command.token
        self.action_label.configure(text=_safe_label(command.action))
        self.detail_label.configure(text=_safe_label(command.detail))

        if not self.window.winfo_viewable():
            self.window.deiconify()
        self.window.lift()
        self.window.attributes("-topmost", True)
        hwnd_topmost = -1
        swp_nomove = 0x0002
        swp_nosize = 0x0001
        swp_noactivate = 0x0010
        swp_showwindow = 0x0040
        user32 = ctypes.windll.user32
        user32.SetWindowPos.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_uint,
        ]
        user32.SetWindowPos.restype = ctypes.c_bool
        user32.SetWindowPos(
            self.hwnd or self.window.winfo_id(),
            ctypes.c_void_p(hwnd_topmost),
            0,
            0,
            0,
            0,
            swp_nomove | swp_nosize | swp_noactivate | swp_showwindow,
        )

    def _hide(self, command: _HideCommand) -> None:
        if command.token is not None and command.token != self._current_token:
            if command.done is not None:
                command.done.set()
            return

        if command.delay > 0:
            token = self._current_token
            self._hide_after_id = self.root.after(
                max(1, int(command.delay * 1000)),
                lambda: self._finish_delayed_hide(token, command.done),
            )
            return

        self._hide_now()
        if command.done is not None:
            command.done.set()

    def _finish_delayed_hide(
        self, token: Optional[int], done: Optional[threading.Event]
    ) -> None:
        self._hide_after_id = None
        if token == self._current_token:
            self._hide_now()
        if done is not None:
            done.set()

    def _hide_now(self) -> None:
        self._cancel_scheduled_hide()
        self._current_token = None
        if self.window is not None:
            self.window.withdraw()

    def _cancel_scheduled_hide(self) -> None:
        if self._hide_after_id is not None:
            try:
                self.root.after_cancel(self._hide_after_id)
            except Exception:
                pass
            self._hide_after_id = None

    def _drain_commands(self) -> None:
        stopping = False
        try:
            for _ in range(100):
                try:
                    command = self.commands.get_nowait()
                except queue.Empty:
                    break

                if isinstance(command, _ShowCommand):
                    self._show(command)
                elif isinstance(command, _HideCommand):
                    self._hide(command)
                elif isinstance(command, _StopCommand):
                    self._hide_now()
                    command.done.set()
                    self.root.quit()
                    stopping = True
                    return
        finally:
            if self.window is not None and not stopping:
                self.root.after(20, self._drain_commands)


class AIActivity:
    """Mutable handle for one visible computer-control activity."""

    def __init__(self, action: str, detail: str = "") -> None:
        self._enabled = _overlay_enabled()
        self._started_at = time.monotonic()
        self._finished = False
        self.token: Optional[int] = None
        if self._enabled:
            self.token = _request_show(action, detail)

    def update(self, action: str, detail: str = "") -> None:
        if self._finished or not self._enabled:
            return
        self.token = _request_show(action, detail)

    def finish(self, min_visible: float = 0.55) -> None:
        if self._finished:
            return
        self._finished = True
        if not self._enabled:
            return
        elapsed = time.monotonic() - self._started_at
        delay = max(0.0, float(min_visible) - elapsed)
        _request_hide(self.token, delay)


_overlay_thread: Optional[_OverlayWindow] = None
_overlay_lock = threading.Lock()
_next_token = 0


def _get_or_start_overlay() -> Optional[_OverlayWindow]:
    global _overlay_thread
    if not _overlay_enabled():
        return None

    with _overlay_lock:
        if _overlay_thread is None:
            _overlay_thread = _OverlayWindow()
            _overlay_thread.start()

        overlay = _overlay_thread

    overlay.ready.wait(timeout=1.5)
    if overlay.failed:
        return None
    return overlay


def _new_token() -> int:
    global _next_token
    with _overlay_lock:
        _next_token += 1
        return _next_token


def _request_show(action: str, detail: str = "") -> Optional[int]:
    overlay = _get_or_start_overlay()
    if overlay is None:
        return None
    token = _new_token()
    overlay.commands.put(_ShowCommand(token, action, detail))
    return token


def _request_hide(token: Optional[int], delay: float = 0.0) -> None:
    overlay = _overlay_thread
    if overlay is None or overlay.failed:
        return
    overlay.commands.put(_HideCommand(token, max(0.0, delay)))


def begin_ai_activity(action: str, detail: str = "") -> AIActivity:
    """Show that the AI is controlling the computer and return a handle."""
    try:
        return AIActivity(action, detail)
    except Exception as exc:
        _log_overlay_error(f"activity overlay unavailable: {exc}")
        activity = AIActivity.__new__(AIActivity)
        activity._enabled = False
        activity._started_at = time.monotonic()
        activity._finished = False
        activity.token = None
        return activity


@contextmanager
def ai_activity(
    action: str, detail: str = "", min_visible: float = 0.55
) -> Iterator[AIActivity]:
    """Context manager that hides the activity indicator afterwards."""
    activity = begin_ai_activity(action, detail)
    try:
        yield activity
    finally:
        activity.finish(min_visible=min_visible)


def hide_overlay(wait: bool = False, timeout: float = 0.35) -> None:
    """Hide immediately, optionally waiting until the window is withdrawn."""
    overlay = _overlay_thread
    if overlay is None or overlay.failed:
        return

    done = threading.Event() if wait else None
    overlay.commands.put(_HideCommand(None, 0.0, done))
    if done is not None:
        done.wait(timeout=max(0.0, timeout))


def prepare_for_screenshot() -> None:
    """Keep the clean capture path explicit and easy to discover."""
    hide_overlay(wait=True)


def shutdown_overlay() -> None:
    """Stop the overlay thread during normal server shutdown."""
    global _overlay_thread
    with _overlay_lock:
        overlay = _overlay_thread
        _overlay_thread = None
    if overlay is None or overlay.failed:
        return

    done = threading.Event()
    overlay.commands.put(_StopCommand(done))
    done.wait(timeout=0.7)


atexit.register(shutdown_overlay)
