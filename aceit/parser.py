"""Parse bullet points from files or CLI args."""

from pathlib import Path


def parse_file(filepath: str) -> list[str]:
    """Read bullet points from a text/markdown file. One bullet per line, blank lines ignored."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    lines = path.read_text().splitlines()
    return _clean_lines(lines)


def parse_args(bullets: list[str]) -> list[str]:
    """Accept bullet points passed as CLI arguments."""
    return _clean_lines(bullets)


def _clean_lines(lines: list[str]) -> list[str]:
    """Strip whitespace, remove leading bullet chars (-, *, •), drop empty lines."""
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Strip common bullet prefixes
        for prefix in ("- ", "* ", "• ", "· "):
            if line.startswith(prefix):
                line = line[len(prefix):]
                break
        cleaned.append(line)
    return cleaned
