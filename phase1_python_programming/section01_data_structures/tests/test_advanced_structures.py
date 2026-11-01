from itertools import count, islice

import pytest

import phase1_python_programming.section01_data_structures.exercises.advanced_structures as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("nums,value", [([], 1), ([1, 3], 2), ([2, 2], 2)])
def test_binary_insert_preserves_input(nums, value):
    before = nums.copy()
    result = m.binary_insert(nums, value)
    assert nums == before
    assert result is not nums


@pytest.mark.parametrize("n", [5, 10, 20])
def test_fibonacci_uses_cache(n):
    first = m.memoized_fibonacci(n)
    info_before = m.memoized_fibonacci.cache_info()
    assert m.memoized_fibonacci(n) == first
    assert m.memoized_fibonacci.cache_info().hits > info_before.hits


@pytest.mark.parametrize(
    "name, size", [("moving_average", 2), ("chunked", 3), ("sliding_window", 2)]
)
def test_window_iterators_are_lazy(name, size):
    consumed = []

    def source():
        for value in range(100):
            consumed.append(value)
            if len(consumed) > 10:
                raise AssertionError("The first output consumed more than one window")
            yield value

    result = getattr(m, name)(source(), size)
    next(iter(result))
    assert len(consumed) <= size


def test_merge_sorted_can_consume_infinite_streams():
    merged = m.merge_sorted(count(0, 2), count(1, 2))
    assert list(islice(merged, 6)) == list(range(6))


@pytest.mark.parametrize(
    "args, expected",
    [((iter([1, 3, 5]), 2), [1, 2, 4]), ((iter([]), 2), []), ((iter([7]), 1), [7])],
)
def test_moving_average(args, expected):
    result = m.moving_average(*args)
    assert iter(result) is result
    assert list(result) == expected


def test_moving_average_invalid():
    with pytest.raises(ValueError):
        list(m.moving_average(iter([1]), 0))


@pytest.mark.parametrize(
    "args, expected",
    [((iter(range(5)), 2), [[0, 1], [2, 3], [4]]), ((iter([]), 2), []), ((iter([1]), 3), [[1]])],
)
def test_chunked(args, expected):
    result = m.chunked(*args)
    assert iter(result) is result
    assert list(result) == expected


def test_chunked_invalid():
    with pytest.raises(ValueError):
        list(m.chunked(iter([1]), 0))


@pytest.mark.parametrize(
    "args, expected",
    [((iter([1, 2, 3]), 2), [(1, 2), (2, 3)]), ((iter([]), 2), []), ((iter([1]), 2), [])],
)
def test_sliding_window(args, expected):
    result = m.sliding_window(*args)
    assert iter(result) is result
    assert list(result) == expected


def test_sliding_window_invalid():
    with pytest.raises(ValueError):
        list(m.sliding_window(iter([1]), 0))


@pytest.mark.parametrize(
    "args, expected",
    [
        ((iter([1, 3]), iter([2])), [1, 2, 3]),
        ((iter([]), iter([])), []),
        ((iter([1, 1]), iter([1])), [1, 1, 1]),
    ],
)
def test_merge_sorted(args, expected):
    result = m.merge_sorted(*args)
    assert list(result) == expected


@pytest.mark.parametrize(
    "args, expected", [(([1, 3], 2), [1, 2, 3]), (([], 1), [1]), (([2, 2], 2), [2, 2, 2])]
)
def test_binary_insert(args, expected):
    result = m.binary_insert(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            ("2025-01-01 12:00:00 INFO ok",),
            {"timestamp": "2025-01-01 12:00:00", "level": "INFO", "message": "ok"},
        ),
        (("",), None),
        (("bad",), None),
        (
            ("2025-01-01 12:00:00 ERROR two words",),
            {"timestamp": "2025-01-01 12:00:00", "level": "ERROR", "message": "two words"},
        ),
    ],
)
def test_parse_log_line(args, expected):
    result = m.parse_log_line(*args)
    assert result == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        (("a@b.com a@b.com",), ["a@b.com"]),
        (("",), []),
        (("x+y@site.org, z@a.cn",), ["x+y@site.org", "z@a.cn"]),
    ],
)
def test_extract_emails(args, expected):
    result = m.extract_emails(*args)
    assert result == expected


@pytest.mark.parametrize("capacity", [1, 2, 3])
def test_lru_cache(capacity):
    cache = m.LRUCache(capacity)
    assert len(cache) == 0
    assert cache.get("absent") == -1
    for i in range(capacity):
        cache.put(i, i)
    assert cache.get(0) == 0
    cache.put("new", 9)
    assert len(cache) == capacity
    assert cache.get(0 if capacity == 1 else 1) == -1
    cache.put("new", 10)
    assert cache.get("new") == 10


@pytest.mark.parametrize("capacity", [0, -1, -10])
def test_lru_invalid(capacity):
    with pytest.raises(ValueError):
        m.LRUCache(capacity)


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (10, 55), (100, 354224848179261915075)])
def test_fibonacci(n, expected):
    assert m.memoized_fibonacci(n) == expected


def test_fibonacci_negative():
    with pytest.raises(ValueError):
        m.memoized_fibonacci(-1)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((iter([1, 2]), iter(["a"])), [(1, "a"), (2, "a")]),
        (([], [1]), []),
        (([1], [2, 3]), [(1, 2), (1, 3)]),
    ],
)
def test_cartesian_pairs(args, expected):
    result = m.cartesian_pairs(*args)
    assert result == expected
