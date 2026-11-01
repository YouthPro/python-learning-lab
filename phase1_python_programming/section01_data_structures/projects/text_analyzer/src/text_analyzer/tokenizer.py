"""A deliberately explicit English tokenization contract."""

import re


def tokenize(text: str, stop_words: set[str] | None = None) -> list[str]:
    """连续 ASCII 英文字母为单词；不含撇号，统一小写。"""
    blocked = {word.lower() for word in (stop_words or set())}
    return [word for word in re.findall(r"[a-z]+", text.lower()) if word not in blocked]
