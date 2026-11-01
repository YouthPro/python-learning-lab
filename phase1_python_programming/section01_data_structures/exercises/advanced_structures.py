from __future__ import annotations

from collections.abc import Iterable, Iterator


def moving_average(stream: Iterable[float], k: int) -> Iterator:
    """13. Moving Average
    Difficulty: Medium
    知识点: deque, iterator, generator

    产生最近最多 k 个元素的均值（含开始时不满窗口的均值）。

    示例: [1,3,5],2 → [1,2,4]；[],2 → []
    边界: 窗口参数≤0 抛 ValueError；惰性读取，不可一次性 list(iterable)。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def chunked(iterable: Iterable, size: int) -> Iterator:
    """14. Chunked Iterator
    Difficulty: Medium
    知识点: deque, iterator, generator

    按 size 产生 list；最后不足 size 的批次保留。

    示例: range(5),2 → [[0,1],[2,3],[4]]；[],2 → []
    边界: 窗口参数≤0 抛 ValueError；惰性读取，不可一次性 list(iterable)。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def sliding_window(iterable: Iterable, k: int) -> Iterator:
    """15. Sliding Window Generator
    Difficulty: Medium
    知识点: deque, iterator, generator

    只产生长度恰好 k 的连续 tuple 窗口。

    示例: [1,2,3],2 → [(1,2),(2,3)]；[1],2 → []
    边界: 窗口参数≤0 抛 ValueError；惰性读取，不可一次性 list(iterable)。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def merge_sorted(a: Iterable, b: Iterable) -> Iterator:
    """16. Merge Sorted Iterables
    Difficulty: Medium
    知识点: heapq, iterator

    惰性合并两个已升序的可迭代对象，保留重复元素。

    示例: [1,3],[2] → [1,2,3]；[],[] → []
    边界: 允许任一输入为空，不可先消费所有输入。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def binary_insert(nums: list[int], value: int) -> list[int]:
    """17. Binary Insert
    Difficulty: Easy
    知识点: bisect

    将 value 插入升序 nums 的合适位置，返回新列表；不修改 nums。

    示例: [1,3],2 → [1,2,3]；[],1 → [1]
    边界: 保留重复值；输入保证已排序。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def parse_log_line(line: str) -> dict | None:
    """18. Log Parser
    Difficulty: Medium
    知识点: re, str

    解析 YYYY-MM-DD HH:MM:SS LEVEL message；LEVEL 仅 INFO/WARNING/ERROR/DEBUG。返回 timestamp、level、message 字段；格式不符返回 None，不校验实际日历。

    示例: "2025-01-01 12:00:00 INFO ok" → {timestamp:...,level:INFO,message:ok}；"bad" → None
    边界: 空串无效；message 可包含空格但非空。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def extract_emails(text: str) -> list[str]:
    """19. Email Extractor
    Difficulty: Easy
    知识点: re

    提取 ASCII 简化邮箱：local 使用字母数字及 ._%+-，域名使用字母数字与 .-，顶级域至少两个字母；保留首次出现顺序并去重。无需实现 RFC 全规范。

    示例: "a@b.com a@b.com" → ["a@b.com"]；"none" → []
    边界: 空输入为 []；原样保留大小写。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


class LRUCache:
    """Exercise 20: 详见 exercise_catalog.md。"""

    def __init__(self, capacity: int):
        # TODO: Implement your solution
        raise NotImplementedError

    def get(self, key):
        # TODO: Implement your solution
        raise NotImplementedError

    def put(self, key, value) -> None:
        # TODO: Implement your solution
        raise NotImplementedError

    def __len__(self) -> int:
        # TODO: Implement your solution
        raise NotImplementedError


def memoized_fibonacci(n: int) -> int:
    """21. Memoized Fibonacci
    Difficulty: Medium
    知识点: functools.cache

    返回 F(0)=0、F(1)=1 的第 n 项；使用 functools.cache 或 lru_cache。

    示例: 0 → 0；10 → 55
    边界: 负数抛 ValueError。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def cartesian_pairs(a: Iterable, b: Iterable) -> list[tuple]:
    """22. Cartesian Product
    Difficulty: Easy
    知识点: itertools.product

    返回按 a 外层、b 内层顺序的笛卡尔积。

    示例: [1,2],["a"] → [(1,"a"),(2,"a")]；[],[1] → []
    边界: 支持一次性迭代器；允许缓存有限输入。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
