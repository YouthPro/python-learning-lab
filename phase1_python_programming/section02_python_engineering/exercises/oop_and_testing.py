from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass


@dataclass
class DatasetRecord:
    """数据记录：为 __len__ 编写实现；保留 dataclass 的 repr 和 eq。"""

    row_id: int
    values: dict

    def __len__(self) -> int:
        # TODO: Implement your solution
        raise NotImplementedError


class DatasetCollection:
    """通过组合维护 DatasetRecord；不要继承 list。"""

    def __init__(self, records: Iterable):
        # TODO: Implement your solution
        raise NotImplementedError

    def add(self, record: DatasetRecord) -> None:
        # TODO: Implement your solution
        raise NotImplementedError

    def __len__(self) -> int:
        # TODO: Implement your solution
        raise NotImplementedError

    def __iter__(self) -> Iterator[DatasetRecord]:
        # TODO: Implement your solution
        raise NotImplementedError

    def __repr__(self) -> str:
        # TODO: Implement your solution
        raise NotImplementedError
