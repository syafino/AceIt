# AceIt

A tiny teleprompter that sits right under your webcam. Feed it your bullet points, navigate with arrow keys, and nail your next interview — while looking like you're making eye contact. The overlay is invisible to screen sharing and screenshots, so you can use it freely without anyone seeing it.

## Requirements

- Python 3.10+
- macOS (tested on macOS 13+)

## Install

```bash
git clone https://github.com/yourusername/AceIt.git
cd AceIt
pip install -e .
```

## Setup (macOS)

AceIt uses global hotkeys so you can navigate bullets even while Zoom or another app has focus. macOS requires you to grant **Accessibility** permissions for this to work:

1. Open **System Settings → Privacy & Security → Accessibility**
2. Add your terminal app (Terminal, iTerm2, VS Code, etc.) to the allowed list
3. You may also need to allow it under **Input Monitoring** in the same section

You only need to do this once.

## Usage

From a file (one bullet per line):
```bash
aceit notes.txt
```

Or pass bullets directly:
```bash
aceit -b "Tell me about yourself" "Why this company?" "Biggest strength"
```

Supports `.txt` and `.md` files. Blank lines are ignored.

### Controls

These work globally — no need to focus the overlay window.

| Key | Action |
|-----|--------|
| → | Next bullet |
| ← | Previous bullet |
| Esc | Quit |

## Example notes.txt

```
Led migration to microservices, cut deploy time 40%
Built real-time dashboard used by 200+ engineers
Why this role: love the product, want to scale it
```

## Tips

- Keep bullets short — a few words to jog your memory, not full sentences.
- Position your webcam at the top center of your screen for the best eye-contact effect.
- Practice cycling through a couple of times before the call starts.
