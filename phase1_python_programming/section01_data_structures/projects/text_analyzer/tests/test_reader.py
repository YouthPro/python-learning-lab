import pytest

from phase1_python_programming.section01_data_structures.projects.text_analyzer.src.text_analyzer.reader import (
    read_lines,
)


@pytest.mark.parametrize("content", ["", "a\nb\n", "hello\n\nworld"])
def test_reader(tmp_path, content):
    p = tmp_path / "a.txt"
    p.write_text(content, encoding="utf-8")
    assert list(read_lines(p)) == content.splitlines(keepends=True)


def test_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(read_lines(tmp_path / "absent"))
