"""Bounded-memory n-gram iterator."""

from collections import deque
from collections.abc import Iterable, Iterator


def iter_ngrams(tokens: Iterable[str], n: int) -> Iterator[tuple[str, ...]]:
    if n <= 0:
        raise ValueError("n must be positive")
    window = deque(maxlen=n)
    for token in tokens:
        window.append(token)
        if len(window) == n:
            yield tuple(window)
