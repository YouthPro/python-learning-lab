from __future__ import annotations

import pandas as pd


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """07. Missing Value Analysis
    Difficulty: Medium
    知识点: isna, sum

    返回以列名为索引的表，列为 missing_count 和 missing_ratio；比例为 0..1，空表比例定义为 0。

    示例: a=[1,None] → count=1,ratio=.5；空 a 列 → 0,0
    边界: 顺序与输入列顺序一致。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """08. Missing Value Imputation
    Difficulty: Medium
    知识点: fillna, median

    返回副本：数值列用该列中位数填充，全缺失数值列用 0；其他列用字符串 unknown；输入为普通 float/object 类型。

    示例: [1,NaN,3] → [1,2,3]；类别 [None] → [unknown]
    边界: 空表保留 shape；不修改输入。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """09. Duplicate Removal
    Difficulty: Easy
    知识点: duplicated

    按整行去重，保留第一次出现，保留原索引。

    示例: a=[1,1,2] → 索引 [0,2]；空表 → 空表
    边界: 两个缺失值视为重复；不修改输入。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def detect_outliers(df: pd.DataFrame, column: str) -> pd.Series:
    """10. Outlier Detection
    Difficulty: Medium
    知识点: quantile, IQR

    用 1.5×IQR 规则返回布尔 Series，严格小于下界或大于上界为异常；缺失值 False；IQR=0 仍按相同公式。

    示例: [1,1,1,1,100] → 最后一项 True；[2,2] → 全 False
    边界: 空列返回空 bool Series；保留索引和列名。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
