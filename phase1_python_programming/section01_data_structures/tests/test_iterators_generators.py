import pytest

import phase1_python_programming.section01_data_structures.exercises.iterators_generators as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "args, expected",
    [((iter([1, 1, 2, 1]),), [(1, 2), (2, 1), (1, 1)]), (([],), []), ((["a", "a"],), [("a", 2)])],
)
def test_group_consecutive(args, expected):
    result = m.group_consecutive(*args)
    assert result == expected


@pytest.mark.parametrize(
    "funcs, value, expected",
    [((str, abs), -2, "2"), ((), 3, 3), ((lambda x: x + 1, lambda x: x * 2), 3, 7)],
)
def test_compose(funcs, value, expected):
    assert m.compose(*funcs)(value) == expected


@pytest.mark.parametrize(
    "args, expected",
    [((int, ["1", "x"]), [1, None]), ((int, []), []), ((lambda x: 1 / x, [0, 2]), [None, 0.5])],
)
def test_safe_map(args, expected):
    result = m.safe_map(*args)
    assert result == expected


@pytest.mark.parametrize("value", [0, -2, 99])
def test_timer(value):
    wrapped = m.timer(abs)
    result, elapsed = wrapped(value)
    assert result == abs(value)
    assert elapsed >= 0
    assert wrapped.__name__ == "abs"


@pytest.mark.parametrize("attempts", [1, 2, 3])
def test_retry(attempts):
    calls = []

    def unstable(value=7):
        calls.append(1)
        if len(calls) < attempts:
            raise ValueError("again")
        return value

    wrapped = m.retry(attempts)(unstable)
    assert wrapped(value=8) == 8
    assert len(calls) == attempts
    assert wrapped.__name__ == "unstable"


@pytest.mark.parametrize("attempts", [1, 2, 3])
def test_retry_exhausted(attempts):
    calls = []

    def fail():
        calls.append(1)
        raise RuntimeError("last")

    wrapped = m.retry(attempts)(fail)
    with pytest.raises(RuntimeError, match="last"):
        wrapped()
    assert len(calls) == attempts


def test_retry_invalid():
    with pytest.raises(ValueError):
        m.retry(0)


@pytest.mark.parametrize(
    "lines, size, expected",
    [(["a", "b", "c"], 2, [["a", "b"], ["c"]]), ([], 2, []), (["x"], 5, [["x"]])],
)
def test_file_batches(tmp_path, lines, size, expected):
    p = tmp_path / "a.txt"
    p.write_text("".join(x + "\n" for x in lines), encoding="utf-8")
    assert list(m.iter_file_batches([p], size)) == expected


def test_batches_cross_file(tmp_path):
    paths = [tmp_path / "a", tmp_path / "b"]
    for path, value in zip(paths, ["x\n", "y\n"]):
        path.write_text(value)
    assert list(m.iter_file_batches(paths, 2)) == [["x", "y"]]


def test_batches_invalid():
    with pytest.raises(ValueError):
        list(m.iter_file_batches([], 0))


@pytest.mark.parametrize(
    "content, expected", [("a\nb\n", ["a", "b"]), ("", []), (" x \n\n", [" x ", ""])]
)
def test_read_lines(tmp_path, content, expected):
    path = tmp_path / "lines.txt"
    path.write_text(content, encoding="utf-8")
    result = m.read_lines(path)
    assert iter(result) is result
    assert list(result) == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        ((["aaa", "b"], len), ["b", "aaa"]),
        (([], len), []),
        ((["ab", "cd", "x"], len), ["x", "ab", "cd"]),
    ],
)
def test_custom_sort(args, expected):
    result = m.custom_sort(*args)
    assert result == expected
