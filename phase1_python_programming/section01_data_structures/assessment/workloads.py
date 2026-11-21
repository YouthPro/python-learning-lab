"""Adversarial inputs and closed-form expectations, without reference exercise solutions.

Preparation and validation are outside both measurement regions. Streaming consumers
keep only a count, checksum and last value, rather than materializing the output.
"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Workload:
    operation: Callable
    validate: Callable


def _equal(expected):
    def validate(actual):
        assert actual == expected, "Stress output differs from the required result"

    return validate


def _drain(iterable, value_of=lambda item: item):
    count, checksum, last = 0, 0, None
    for last in iterable:
        count += 1
        checksum += value_of(last)
    return count, checksum, last


def _identity(value):
    return value


def make_workload(name: str, target: Callable, directory: Path) -> Workload:
    if name == "word_frequency":
        words = ["w" + chr(97 + i // 26) + chr(97 + i % 26) for i in range(64)]
        text = " ".join(words * 4687 + words[:32])
        return Workload(
            lambda: target(text), _equal({w: 4687 + (i < 32) for i, w in enumerate(words)})
        )
    if name == "first_unique_char":
        text = "a" * 300_000 + "b"
        return Workload(lambda: target(text), _equal(300_000))
    if name == "deduplicate":
        values = list(range(100_000)) * 2
        return Workload(lambda: target(values), _equal(list(range(100_000))))
    if name == "two_sum":
        n = 120_000
        values = list(range(n))
        return Workload(lambda: target(values, 2 * n - 3), _equal([n - 2, n - 1]))
    if name == "group_anagrams":
        # Distinct Unicode characters prevent accidental cross-group anagrams.
        words = [
            word for i in range(30_000) for word in (chr(0x1000 + i) + "a", "a" + chr(0x1000 + i))
        ]
        return Workload(
            lambda: target(words), _equal([words[i : i + 2] for i in range(0, len(words), 2)])
        )
    if name == "top_k_frequent":
        values = list(range(99_999, -1, -1)) * 2
        return Workload(lambda: target(values, 10), _equal(list(range(10))))
    if name == "merge_intervals":
        intervals = [[3 * i, 3 * i + 1] for i in range(59_999, -1, -1)]
        expected = list(reversed(intervals))
        return Workload(lambda: target(intervals), _equal(expected))
    if name == "longest_unique_substring":
        text = "".join(chr(0x1000 + i) for i in range(10_000)) * 10
        return Workload(lambda: target(text), _equal(10_000))
    if name == "is_valid_parentheses":
        text = "(" * 100_000 + ")" * 100_000
        return Workload(lambda: target(text), _equal(True))
    if name == "flatten_list":
        items = [[i, [i + 1, i + 2]] for i in range(60_000)]
        return Workload(
            lambda: target(items), _equal([v for i in range(60_000) for v in (i, i + 1, i + 2)])
        )
    if name in {"rotate_matrix", "transpose_matrix"}:
        rows, cols = (600, 600) if name == "rotate_matrix" else (400, 900)
        matrix = [[r * cols + c for c in range(cols)] for r in range(rows)]

        def validate(actual):
            assert len(actual) == cols
            assert all(len(row) == rows for row in actual)
            for r, row in enumerate(actual):
                for c, value in enumerate(row):
                    expected = (
                        (rows - 1 - c) * cols + r if name == "rotate_matrix" else c * cols + r
                    )
                    assert value == expected
            assert matrix[0][0] == 0 and matrix[-1][-1] == rows * cols - 1

        return Workload(lambda: target(matrix), validate)
    if name == "moving_average":
        n, k = 120_000, 1024
        # Exactly representable half-integer averages, even during warm-up.
        expected_sum = sum(i / 2 if i < k else i - (k - 1) / 2 for i in range(n))
        return Workload(
            lambda: _drain(target(iter(range(n)), k)),
            _equal((n, expected_sum, n - 1 - (k - 1) / 2)),
        )
    if name == "chunked":
        n, k = 200_000, 128
        return Workload(
            lambda: _drain(target(iter(range(n)), k), sum),
            _equal(((n + k - 1) // k, n * (n - 1) // 2, list(range(n // k * k, n)))),
        )
    if name == "sliding_window":
        n, k = 80_000, 32
        count = n - k + 1
        expected_sum = k * count * (count - 1) // 2 + count * k * (k - 1) // 2
        return Workload(
            lambda: _drain(target(iter(range(n)), k), sum),
            _equal((count, expected_sum, tuple(range(n - k, n)))),
        )
    if name == "merge_sorted":
        n = 200_000
        return Workload(
            lambda: _drain(target(iter(range(0, n, 2)), iter(range(1, n, 2)))),
            _equal((n, n * (n - 1) // 2, n - 1)),
        )
    if name == "binary_insert":
        values = list(range(0, 400_000, 2))
        expected = values[:100_000] + [199_999] + values[100_000:]

        def validate(actual):
            assert actual == expected and actual is not values
            assert len(values) == 200_000 and values[100_000] == 200_000

        return Workload(lambda: target(values, 199_999), validate)
    if name == "parse_log_line":
        line = "2025-01-01 12:00:00 INFO ready"
        malformed = "x" * 300_000

        def operation():
            valid = 0
            for _ in range(20_000):
                row = target(line)
                valid += row == {
                    "timestamp": "2025-01-01 12:00:00",
                    "level": "INFO",
                    "message": "ready",
                }
            return valid, target(malformed)

        return Workload(operation, _equal((20_000, None)))
    if name == "extract_emails":
        emails = [f"person{i}@example.com" for i in range(32)]
        text = " ".join(emails * 1562 + emails[:16])
        return Workload(lambda: target(text), _equal(emails))
    if name == "LRUCache":
        capacity, operations = 4096, 30_000

        def operation():
            cache = target(capacity)
            for i in range(capacity):
                cache.put(i, i)
            checksum = 0
            for i in range(operations):
                key = i % capacity
                checksum += cache.get(key)
                cache.put(key, key)
            # Fresh insertions also distinguish capacity-bounded caches from leaks.
            for i in range(operations):
                cache.put(capacity + i, i)
            return checksum, len(cache), cache.get(0), cache.get(capacity + operations - 1)

        expected_sum = (operations // capacity) * capacity * (capacity - 1) // 2 + sum(
            range(operations % capacity)
        )
        return Workload(operation, _equal((expected_sum, capacity, -1, operations - 1)))
    if name == "memoized_fibonacci":

        def operation():
            first = target(32)
            return first, sum(target(32) for _ in range(1000))

        return Workload(operation, _equal((2178309, 2178309000)))
    if name == "cartesian_pairs":
        n = 500

        def validate(actual):
            assert isinstance(actual, list) and len(actual) == n * n
            for i, pair in enumerate(actual):
                assert pair == divmod(i, n)

        return Workload(lambda: target(iter(range(n)), iter(range(n))), validate)
    if name == "group_consecutive":
        expected = [(i, 4) for i in range(50_000)]
        return Workload(lambda: target(i // 4 for i in range(200_000)), _equal(expected))
    if name == "compose":
        functions = (_identity,) * 64

        def operation():
            composed = target(*functions)
            return sum(composed(i) for i in range(5000))

        return Workload(operation, _equal(4999 * 5000 // 2))
    if name == "safe_map":
        expected = [7, None] * 50_000
        return Workload(
            lambda: target(int, ("7" if i % 2 == 0 else "bad" for i in range(100_000))),
            _equal(expected),
        )
    if name == "timer":

        def operation():
            wrapped = target(_identity)
            checksum, valid = 0, True
            for i in range(50_000):
                value, elapsed = wrapped(i)
                checksum += value
                valid = valid and elapsed >= 0
            return checksum, valid, wrapped.__name__

        return Workload(operation, _equal((49_999 * 50_000 // 2, True, "_identity")))
    if name == "retry":
        attempts = 0

        def callback():
            nonlocal attempts
            attempts += 1
            if attempts % 3:
                raise ValueError("try again")
            return 7

        def operation():
            nonlocal attempts
            attempts = 0
            wrapped = target(3)(callback)
            return sum(wrapped() for _ in range(10_000)), attempts, wrapped.__name__

        return Workload(operation, _equal((70_000, 30_000, "callback")))
    if name in {"iter_file_batches", "read_lines"}:
        line = "x" * 63 + "\n"
        directory.mkdir(parents=True, exist_ok=True)
        paths = [directory / "a.txt", directory / "b.txt"]
        for path in paths:
            with path.open("w", encoding="utf-8", newline="") as handle:
                for _ in range(60_000):
                    handle.write(line)
        if name == "read_lines":
            # One file with the full 120k-line workload.
            with paths[0].open("a", encoding="utf-8", newline="") as handle:
                for _ in range(60_000):
                    handle.write(line)
            return Workload(
                lambda: _drain(target(paths[0]), len), _equal((120_000, 120_000 * 63, "x" * 63))
            )
        return Workload(
            lambda: _drain(target(iter(paths), 128), lambda batch: sum(map(len, batch))),
            _equal((938, 120_000 * 63, ["x" * 63] * 64)),
        )
    if name == "custom_sort":
        # Coprime multiplier permutes the full integer range, avoiding a presorted case.
        values = [(i * 7919) % 100_000 for i in range(100_000)]
        return Workload(
            lambda: target(iter(values), lambda x: x // 10),
            _equal(sorted(values, key=lambda x: x // 10)),
        )
    raise ValueError(f"No workload for {name}")
