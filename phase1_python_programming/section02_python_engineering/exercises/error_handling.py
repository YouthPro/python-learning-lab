from __future__ import annotations

import logging
from pathlib import Path


class DatasetError(Exception):
    """统一包装数据加载错误；保留原始异常原因。"""


def load_json_safely(path: str | Path, logger: logging.Logger) -> object:
    """07. Logged JSON Loader
    Difficulty: Medium
    知识点: custom exception, try/except, logging

    读取 UTF-8 JSON，文件或 JSON 错误时记录 ERROR 并抛自定义 DatasetError，使用 raise ... from ... 保留原因。

    示例: 合法 {"a":1} → dict；非法 JSON → DatasetError + ERROR 日志
    边界: 成功不记 ERROR；缺失路径、空文件均为失败。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
