"""Transparent always-on-top overlay window for displaying bullet points."""

import tkinter as tk


class Overlay:
    """Floating teleprompter window that sits just under the webcam."""

    BG_COLOR = "#1a1a1a"
    FG_COLOR = "#f0f0f0"
    FONT = ("SF Pro Display", 20)
    PADDING_X = 40
    PADDING_Y = 12
    OPACITY = 0.85

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

        self.label = tk.Label(
            self.root,
            text="",
            font=self.FONT,
            fg=self.FG_COLOR,
            bg=self.BG_COLOR,
            wraplength=600,
            justify="center",
            padx=self.PADDING_X,
            pady=self.PADDING_Y,
        )
        self.label.pack()

        self.counter = tk.Label(
            self.root,
            text="",
            font=("SF Pro Display", 11),
            fg="#888888",
            bg=self.BG_COLOR,
        )
        self.counter.pack(pady=(0, 8))

        # Key bindings
        self.root.bind("<Right>", lambda e: self.next())
        self.root.bind("<Left>", lambda e: self.prev())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

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

    def next(self):
        if self.index < len(self.bullets) - 1:
            self.index += 1
            self._update_display()

    def prev(self):
        if self.index > 0:
            self.index -= 1
            self._update_display()

    def run(self):
        self.root.mainloop()
