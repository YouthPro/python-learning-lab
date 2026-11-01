"""逐行读取；生成器关闭时文件句柄也随 with 关闭。"""

from collections.abc import Iterator
from pathlib import Path


def read_lines(path: str | Path) -> Iterator[str]:
    """保留原始换行，供字符数统计使用。"""
    with Path(path).open(encoding="utf-8") as handle:
        yield from handle
