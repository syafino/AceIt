# AceIt

A tiny teleprompter that sits right under your webcam. Feed it your bullet points, navigate with arrow keys, and nail your next interview — while looking like you're making eye contact.

## Install

```bash
git clone https://github.com/yourusername/AceIt.git
cd AceIt
pip install -e .
```

## Usage

From a file (one bullet per line):
```bash
aceit notes.txt
```

Or pass bullets directly:
```bash
aceit -b "Tell me about yourself" "Why this company?" "Biggest strength"
```

### Controls

| Key | Action |
|-----|--------|
| Right arrow | Next bullet |
| Left arrow | Previous bullet |
| Esc | Quit |

## Example notes.txt

```
- Led migration to microservices, cut deploy time 40%
- Built real-time dashboard used by 200+ engineers
- Why this role: love the product, want to scale it
```
