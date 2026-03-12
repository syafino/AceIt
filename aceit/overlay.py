"""Transparent always-on-top overlay window for displaying bullet points."""

import tkinter as tk

from pynput import keyboard


def _set_macos_floating(root):
    """Use macOS native API to float above all apps and hide from screen sharing."""
    try:
        from ctypes import cdll, c_void_p, c_long

        objc = cdll.LoadLibrary("/usr/lib/libobjc.dylib")
        objc.objc_getClass.restype = c_void_p
        objc.sel_registerName.restype = c_void_p
        objc.objc_msgSend.restype = c_void_p
        objc.objc_msgSend.argtypes = [c_void_p, c_void_p]

        NSApp = objc.objc_msgSend(
            objc.objc_getClass(b"NSApplication"),
            objc.sel_registerName(b"sharedApplication"),
        )
        windows = objc.objc_msgSend(NSApp, objc.sel_registerName(b"windows"))
        count = objc.objc_msgSend(windows, objc.sel_registerName(b"count"))

        set_level = objc.sel_registerName(b"setLevel:")
        set_sharing = objc.sel_registerName(b"setSharingType:")
        for i in range(count):
            objc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_long]
            win = objc.objc_msgSend(
                windows, objc.sel_registerName(b"objectAtIndex:"), c_long(i)
            )
            # kCGFloatingWindowLevel = 3 (above normal windows, including Zoom)
            objc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_long]
            objc.objc_msgSend(win, set_level, c_long(3))
            # NSWindowSharingNone = 0 (invisible to screen capture/sharing)
            objc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_long]
            objc.objc_msgSend(win, set_sharing, c_long(0))
    except Exception:
        pass  # Fall back to tkinter's -topmost


class Overlay:
    """Floating teleprompter window that sits just under the webcam."""

    BG_COLOR = "#1a1a1a"
    FG_COLOR = "#f0f0f0"
    FONT = ("SF Pro Display", 14)
    PADDING_X = 20
    PADDING_Y = 6
    OPACITY = 0.85
    TOPMOST_INTERVAL_MS = 2000  # Re-assert topmost every 2 seconds

    def __init__(self, bullets: list[str]):
        if not bullets:
            raise ValueError("No bullet points to display")

        self.bullets = bullets
        self.index = 0

        self.root = tk.Tk()
        self.root.title("AceIt")
        self.root.overrideredirect(True)  # Borderless
        self.root.attributes("-topmost", True)  # Always on top
        self.root.attributes("-alpha", self.OPACITY)
        self.root.configure(bg=self.BG_COLOR)

        # Set macOS floating panel level so it stays above Zoom, etc.
        self.root.after(100, lambda: _set_macos_floating(self.root))

        self.label = tk.Label(
            self.root,
            text="",
            font=self.FONT,
            fg=self.FG_COLOR,
            bg=self.BG_COLOR,
            wraplength=400,
            justify="center",
            padx=self.PADDING_X,
            pady=self.PADDING_Y,
        )
        self.label.pack()

        self.counter = tk.Label(
            self.root,
            text="",
            font=("SF Pro Display", 9),
            fg="#888888",
            bg=self.BG_COLOR,
        )
        self.counter.pack(pady=(0, 8))

        # Local key bindings (when overlay has focus)
        self.root.bind("<Right>", lambda e: self.next())
        self.root.bind("<Left>", lambda e: self.prev())
        self.root.bind("<Escape>", lambda e: self.quit())

        # Global hotkey listener (works even when Zoom/other apps have focus)
        self._listener = keyboard.Listener(on_press=self._on_global_key)
        self._listener.daemon = True
        self._listener.start()

        self._update_display()
        self._center_top()

    def _center_top(self):
        """Position window at top-center of the screen, just under the webcam."""
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        win_w = self.root.winfo_width()
        x = (screen_w - win_w) // 2
        y = 5  # Just below the top edge / camera
        self.root.geometry(f"+{x}+{y}")

    def _update_display(self):
        self.label.config(text=self.bullets[self.index])
        self.counter.config(text=f"{self.index + 1} / {len(self.bullets)}")
        self._center_top()  # Re-center in case text width changed

    def _on_global_key(self, key):
        """Handle global key presses from any app."""
        if key == keyboard.Key.right:
            self.root.after(0, self.next)
        elif key == keyboard.Key.left:
            self.root.after(0, self.prev)
        elif key == keyboard.Key.esc:
            self.root.after(0, self.quit)

    def next(self):
        if self.index < len(self.bullets) - 1:
            self.index += 1
            self._update_display()

    def prev(self):
        if self.index > 0:
            self.index -= 1
            self._update_display()

    def quit(self):
        self._listener.stop()
        self.root.destroy()

    def _keep_on_top(self):
        """Periodically re-assert topmost so macOS doesn't drop it when other apps gain focus."""
        self.root.attributes("-topmost", False)
        self.root.attributes("-topmost", True)
        self.root.after(self.TOPMOST_INTERVAL_MS, self._keep_on_top)

    def run(self):
        self.root.after(self.TOPMOST_INTERVAL_MS, self._keep_on_top)
        self.root.mainloop()
