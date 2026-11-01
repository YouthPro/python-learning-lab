import pytest

from phase1_python_programming.section01_data_structures.projects.text_analyzer.src.text_analyzer.tokenizer import (
    tokenize,
)


@pytest.mark.parametrize(
    "text, stops, expected",
    [("Hi hi!", set(), ["hi", "hi"]), ("", set(), []), ("A, cat's 123", {"a", "s"}, ["cat"])],
)
def test_tokens(text, stops, expected):
    assert tokenize(text, stops) == expected
