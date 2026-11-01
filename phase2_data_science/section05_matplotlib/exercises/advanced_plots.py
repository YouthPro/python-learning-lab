from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def plot_correlation(df: pd.DataFrame) -> tuple[Figure, Axes]:
    """06. Correlation Heatmap
    Difficulty: Medium
    知识点: imshow, colorbar

    对数值列计算 Pearson 相关性，用 imshow 显示，色域固定 [-1,1]，附 colorbar 和列名刻度、标题及轴标签。

    示例: 两列 → 2×2 图像；一列 → 1×1 图像
    边界: 没有数值列抛 ValueError；常数列 NaN 保留。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def plot_dashboard(data: dict[str, Sequence[float]]) -> tuple[Figure, np.ndarray]:
    """07. Multiple Subplots
    Difficulty: Medium
    知识点: subplots

    输入 x、y、values；创建 2×2 子图：依次为 x/y 折线、x/y 散点、values 直方、values 箱线；每幅有标题和轴标签。

    示例: x=[1,2],y=[3,4],values=[1,2] → 4 子图；空序列 → 空图
    边界: 返回 fig 与 shape (2,2) 的 axes；不 show。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def save_figure(fig: Figure, path: str | Path) -> Path:
    """08. Save Figure
    Difficulty: Easy
    知识点: savefig, pathlib

    创建父目录，以 PNG 格式、dpi=150、bbox_inches=tight 保存图像，返回 Path。

    示例: fig,out/a.png → 创建文件并返回 Path；空白 fig → 合法 PNG
    边界: 不关闭调用方 fig；不依赖桌面环境。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
