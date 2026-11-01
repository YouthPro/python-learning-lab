"""文件边界切断 n-gram；单个文件内 n-gram 跨行。"""

from collections import Counter
from collections.abc import Iterable
from pathlib import Path

from .ngram import iter_ngrams
from .reader import read_lines
from .tokenizer import tokenize


def analyze_files(paths: Iterable[str | Path], stop_words: set[str] | None = None) -> dict:
    words: Counter = Counter()
    bigrams: Counter = Counter()
    trigrams: Counter = Counter()
    chars = raw_count = 0
    blocked = {word.lower() for word in (stop_words or set())}

    def tokens_from_file(path):
        nonlocal chars, raw_count
        for line in read_lines(path):
            chars += len(line)
            tokens = tokenize(line)
            raw_count += len(tokens)
            for token in tokens:
                if token not in blocked:
                    words[token] += 1
                    yield token

    for path in paths:
        previous = None
        for pair in iter_ngrams(tokens_from_file(path), 2):
            bigrams[" ".join(pair)] += 1
            if previous is not None:
                trigrams[" ".join((previous[0], *pair))] += 1
            previous = pair
    ordered = sorted(words.items(), key=lambda pair: (-pair[1], pair[0]))
    return {
        "total_characters": chars,
        "total_words": raw_count,
        "filtered_words": sum(words.values()),
        "unique_words": len(words),
        "top_20": ordered[:20],
        "word_frequency": dict(ordered),
        "bigrams": dict(sorted(bigrams.items())),
        "trigrams": dict(sorted(trigrams.items())),
    }
