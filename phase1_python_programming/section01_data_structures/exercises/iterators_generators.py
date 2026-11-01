from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from pathlib import Path


def group_consecutive(items: Iterable) -> list[tuple]:
    """23. Consecutive Grouping
    Difficulty: Medium
    知识点: itertools.groupby

    将相邻相等元素压缩为 (value,count)，不合并不相邻的同值元素。

    示例: [1,1,2,1] → [(1,2),(2,1),(1,1)]；[] → []
    边界: 接受一次性迭代器。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def compose(*functions: Callable) -> Callable:
    """24. Compose Functions
    Difficulty: Medium
    知识点: closures, functional

    从右到左组合一元函数；无函数时返回恒等函数。

    示例: compose(str,abs)(-2) → "2"；compose()(3) → 3
    边界: 保留函数异常。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def safe_map(func: Callable, iterable: Iterable) -> list:
    """25. Safe Map
    Difficulty: Medium
    知识点: exceptions, map

    对每个元素应用 func，遇到 Exception 时在对应位置返回 None，继续处理；不捕获 BaseException。

    示例: int,["1","x"] → [1,None]；int,[] → []
    边界: 保持长度和顺序。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def timer(func: Callable) -> Callable:
    """26. Timer Decorator
    Difficulty: Medium
    知识点: decorator, wraps, perf_counter

    包装函数，返回 (原返回值,耗时秒数)，用 perf_counter 计时，保留 __name__；异常原样传播。

    示例: timer(abs)(-2) → (2,非负秒数)；timer(len)([]) → (0,非负秒数)
    边界: 支持位置和关键字参数；不输出 stdout。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def retry(max_attempts: int) -> Callable:
    """27. Retry Decorator
    Difficulty: Medium
    知识点: decorator, closure, wraps

    遇到 Exception 重试，最多执行 max_attempts 次；成功立即返回，失败重新抛最后一次异常。保留元数据。

    示例: retry(2) 包装首次失败函数 → 第二次成功；retry(1) → 不重试
    边界: max_attempts≤0 在创建装饰器时抛 ValueError；不捕获 BaseException。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def iter_file_batches(paths: Iterable[Path], size: int) -> Iterator[list[str]]:
    """28. Batch File Generator
    Difficulty: Medium
    知识点: generator, files

    按 paths 顺序逐行读取 UTF-8 文件，移除换行符，每 size 行产生一个 list；批次可跨文件。

    示例: 两个文件各一行，size=2 → [["a","b"]]；空 paths → []
    边界: size≤0 抛 ValueError；尾批保留；文件异常传播；不可整体读文件。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def read_lines(path: str | Path) -> Iterator[str]:
    """29. Lazy Line Reader
    Difficulty: Easy
    知识点: yield, context manager

    逐行读取 UTF-8 文本，去掉末尾 CR/LF，其余空白保留。

    示例: 文件 "a\nb\n" → ["a","b"]；空文件 → []
    边界: 使用 with 关闭文件；不存在路径抛 FileNotFoundError。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def custom_sort(items: Iterable, key_func: Callable) -> list:
    """30. Custom Sort
    Difficulty: Easy
    知识点: sorted, key

    按 key_func 升序稳定排序，返回新列表。

    示例: ["aaa","b"],len → ["b","aaa"]；[],len → []
    边界: 相同 key 保持输入顺序。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
