import csv
import json

import pytest

from phase1_python_programming.section01_data_structures.projects.text_analyzer.src.text_analyzer.analyzer import (
    analyze_files,
)
from phase1_python_programming.section01_data_structures.projects.text_analyzer.src.text_analyzer.reporter import (
    save_report,
)


@pytest.mark.parametrize(
    "content,words",
    [("", {}), ("A a b", {"a": 2, "b": 1}), ("One\ntwo three", {"one": 1, "three": 1, "two": 1})],
)
def test_analysis(tmp_path, content, words):
    p = tmp_path / "a.txt"
    p.write_text(content)
    report = analyze_files([p])
    assert report["total_characters"] == len(content)
    assert report["word_frequency"] == words
    assert report["total_words"] == sum(words.values())
    jp, cp = save_report(report, tmp_path / "out")
    assert json.loads(jp.read_text())["word_frequency"] == words
    with cp.open() as f:
        assert len(list(csv.DictReader(f))) == len(words)


def test_boundaries_and_stop_words(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_text("a stop\nb c")
    b.write_text("d e")
    result = analyze_files([a, b], {"stop"})
    assert result["total_words"] == 6
    assert result["filtered_words"] == 5
    assert result["bigrams"] == {"a b": 1, "b c": 1, "d e": 1}
    assert result["trigrams"] == {"a b c": 1}


def test_streaming(tmp_path, monkeypatch):
    # A read()/readlines() call would fail; iteration remains available.
    from pathlib import Path

    original = Path.open

    class IterationOnly:
        def __init__(self, handle):
            self.handle = handle

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.handle.close()

        def __iter__(self):
            return iter(self.handle)

        def read(self, *args):
            raise AssertionError("whole-file read")

        def readlines(self, *args):
            raise AssertionError("whole-file read")

    p = tmp_path / "large"
    p.write_text("hello world\n" * 10000)
    monkeypatch.setattr(
        Path, "open", lambda self, *a, **kw: IterationOnly(original(self, *a, **kw))
    )
    assert analyze_files([p])["total_words"] == 20000
