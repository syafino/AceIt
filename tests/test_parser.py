from aceit.parser import parse_file, parse_args, _clean_lines


def test_clean_lines_strips_bullets():
    lines = ["- First point", "* Second point", "• Third point", "Plain line"]
    result = _clean_lines(lines)
    assert result == ["First point", "Second point", "Third point", "Plain line"]


def test_clean_lines_skips_empty():
    lines = ["Hello", "", "  ", "World"]
    result = _clean_lines(lines)
    assert result == ["Hello", "World"]


def test_parse_args():
    result = parse_args(["- Tell me about yourself", "Why this role?"])
    assert result == ["Tell me about yourself", "Why this role?"]


def test_parse_file(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_text("- Intro\n- Experience\n\n- Why me\n")
    result = parse_file(str(f))
    assert result == ["Intro", "Experience", "Why me"]
