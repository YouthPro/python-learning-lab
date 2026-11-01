from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_dataset(path: str | Path) -> pd.DataFrame:
    """01. Load Dataset
    Difficulty: Easy
    知识点: read_csv

    加载带表头 CSV，按 Pandas 默认规则推断 dtype。

    示例: a,b\n1,2 → 一行两列；仅表头 a,b → 零行两列
    边界: 零字节文件抛 pd.errors.EmptyDataError；路径缺失传播异常。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """02. Select Columns
    Difficulty: Easy
    知识点: loc, copy

    按 columns 给定顺序选择列并返回独立副本，保留索引。

    示例: a,b 选择 [b,a] → b,a；选择 [] → 无列
    边界: 缺失列抛 KeyError；支持空行。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def filter_rows(df: pd.DataFrame, condition: pd.Series) -> pd.DataFrame:
    """03. Conditional Filtering
    Difficulty: Easy
    知识点: boolean indexing

    用与 df 索引对齐的布尔 Series 筛选，NA 当 False，保留原索引。

    示例: a=[1,2],mask=[False,True] → 第二行；全 False → 空表
    边界: 空表合法；不修改输入。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def transform_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """04. Column Transformation
    Difficulty: Easy
    知识点: map, strings

    返回副本，将指定字符串列去首尾空白并小写；缺失值保持缺失。

    示例: [" A ","B"] → ["a","b"]；[None] → [None]
    边界: 空表合法；其他列与索引不变。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def convert_dates(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """05. Date Conversion
    Difficulty: Medium
    知识点: to_datetime

    在副本中把指定 ISO 日期字符串列转 datetime64[ns]；无效值与缺失值为 NaT。

    示例: ["2025-01-01","bad"] → [Timestamp,NaT]；空列 → datetime 空列
    边界: 保留索引；不修改输入。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """06. Data Type Conversion
    Difficulty: Medium
    知识点: nullable dtypes, convert_dtypes

    使用 Pandas 可空类型自动转换列（等同 df.convert_dtypes() 的默认 numpy_nullable 后端），返回新表。

    示例: [1,None] → Int64；[True,None] → boolean
    边界: 空表合法；字符串保留 string dtype。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
