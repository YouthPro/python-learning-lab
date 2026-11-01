import pytest

import phase1_python_programming.section01_data_structures.exercises.basic_structures as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "args, expected", [(("Hi hi!",), {"hi": 2}), (("",), {}), (("A,b 123 a",), {"a": 2, "b": 1})]
)
def test_word_frequency(args, expected):
    result = m.word_frequency(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected", [(("leetcode",), 0), (("",), -1), (("aabb",), -1), (("aab c",), 2)]
)
def test_first_unique_char(args, expected):
    result = m.first_unique_char(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected", [(([2, 1, 2],), [2, 1]), (([],), []), ((["a", "a", 2],), ["a", 2])]
)
def test_deduplicate(args, expected):
    result = m.deduplicate(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [(([2, 7, 11], 9), [0, 1]), (([], 0), []), (([3, 3], 6), [0, 1]), (([-1, 2, 3], 2), [0, 2])],
)
def test_two_sum(args, expected):
    result = m.two_sum(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        ((["ab", "ba", "c"],), [["ab", "ba"], ["c"]]),
        (([],), []),
        ((["", "", "A", "a"],), [["", ""], ["A"], ["a"]]),
    ],
)
def test_group_anagrams(args, expected):
    result = m.group_anagrams(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [(([2, 1, 2, 1, 3], 2), [1, 2]), (([], 3), []), (([9], 5), [9]), (([1], 0), [])],
)
def test_top_k_frequent(args, expected):
    result = m.top_k_frequent(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [(([[1, 3], [2, 4]],), [[1, 4]]), (([],), []), (([[3, 3], [1, 3], [2, 2]],), [[1, 3]])],
)
def test_merge_intervals(args, expected):
    result = m.merge_intervals(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected", [(("abcabcbb",), 3), (("",), 0), (("bb",), 1), (("你好吗你",), 3)]
)
def test_longest_unique_substring(args, expected):
    result = m.longest_unique_substring(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected", [(("([])",), True), (("",), True), (("([)]",), False), (("a",), False)]
)
def test_is_valid_parentheses(args, expected):
    result = m.is_valid_parentheses(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [(([1, [2, [3]]],), [1, 2, 3]), (([],), []), (([[], (1, 2), "hi"],), [(1, 2), "hi"])],
)
def test_flatten_list(args, expected):
    result = m.flatten_list(*args)
    assert result == expected


@pytest.mark.parametrize(
    "matrix, expected", [([[1, 2], [3, 4]], [[3, 1], [4, 2]]), ([], []), ([[5]], [[5]])]
)
def test_rotate_matrix(matrix, expected):
    before = [row[:] for row in matrix]
    assert m.rotate_matrix(matrix) == expected
    assert matrix == before


def test_rotate_invalid():
    with pytest.raises(ValueError):
        m.rotate_matrix([[1, 2]])


@pytest.mark.parametrize(
    "a, expected", [([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]), ([], []), ([[]], [])]
)
def test_transpose_matrix(a, expected):
    assert m.transpose_matrix(a) == expected


def test_transpose_invalid():
    with pytest.raises(ValueError):
        m.transpose_matrix([[1], [2, 3]])
