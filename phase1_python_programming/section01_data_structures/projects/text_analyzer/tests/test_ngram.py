import pytest

from phase1_python_programming.section01_data_structures.projects.text_analyzer.src.text_analyzer.ngram import (
    iter_ngrams,
)


@pytest.mark.parametrize(
    "tokens,n,expected",
    [(["a", "b", "c"], 2, [("a", "b"), ("b", "c")]), ([], 2, []), (["a"], 3, [])],
)
def test_ngram(tokens, n, expected):
    assert list(iter_ngrams(iter(tokens), n)) == expected


@pytest.mark.parametrize("n", [0, -1, -10])
def test_invalid(n):
    with pytest.raises(ValueError):
        list(iter_ngrams([], n))
