from __future__ import annotations

import pandas as pd


def group_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """11. Group Statistics
    Difficulty: Medium
    知识点: groupby, agg

    输入列 category、amount；按 category 分组（缺失组丢弃），输出 sum、mean、count；category 为排序索引。

    示例: A:1,A:3 → A sum=4 mean=2 count=2；空输入 → 空结果
    边界: amount 的 NaN 不参与 count；分类列为普通字符串。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def group_transform(df: pd.DataFrame) -> pd.DataFrame:
    """12. Group Transformation
    Difficulty: Medium
    知识点: transform

    输入 category、amount；返回副本，新增 category_mean 为同类别 amount 均值，保持行顺序和索引。

    示例: A:1,A:3 → category_mean=[2,2]；B:8 → 8
    边界: 缺失类别的均值为 NaN；空输入支持。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def merge_tables(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
    """13. Merge Tables
    Difficulty: Medium
    知识点: merge, validate

    按 user_id 左连接，right 的 user_id 必须唯一，使用 validate=many_to_one，保留左表顺序。

    示例: left id=[1,2],right id=[1] → 两行，第二行右列缺失；空左表 → 空表
    边界: 重复右键抛 pd.errors.MergeError；列重名使用默认 _x/_y。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def create_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """14. Pivot Data
    Difficulty: Medium
    知识点: pivot_table

    输入 city、category、amount；以 city 为索引、category 为列，求销售额 sum，缺失组合填 0，排序行列。

    示例: X,A:2 与 X,B:3 → X 行 [2,3]；同组合多行求和
    边界: 空表支持；使用 observed=True。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def rolling_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """15. Rolling Average
    Difficulty: Medium
    知识点: rolling

    输入按时间排好的 amount 列；返回副本，增加 rolling_mean，使用 window 和 min_periods=1；不重新排序。

    示例: [1,3,5],2 → [1,2,4]；[],2 → []
    边界: window≤0 抛 ValueError；缺失数值按 Pandas rolling 规则。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
