from __future__ import annotations

from collections.abc import Sequence

from matplotlib.axes import Axes
from matplotlib.figure import Figure


def plot_line(x: Sequence, y: Sequence) -> tuple[Figure, Axes]:
    """01. Line Plot
    Difficulty: Easy
    知识点: Figure, Axes, labels

    绘制一条标记为 data 的曲线，设置标题、x/y 标签。 返回 (fig,ax)，不调用 show()。

    示例: [0,1],[2,3] → 一条线；[],[] → 空数据曲线
    边界: 空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def plot_bar(categories: Sequence[str], values: Sequence[float]) -> tuple[Figure, Axes]:
    """02. Bar Chart
    Difficulty: Easy
    知识点: Figure, Axes, labels

    绘制柱形图，设置标题、x/y 标签。 返回 (fig,ax)，不调用 show()。

    示例: [A,B],[1,2] → 两根柱；[],[] → 无柱
    边界: 空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def plot_hist(data: Sequence[float]) -> tuple[Figure, Axes]:
    """03. Histogram
    Difficulty: Easy
    知识点: Figure, Axes, labels

    绘制 10 个 bin 的直方图，设置标题、x/y 标签。 返回 (fig,ax)，不调用 show()。

    示例: [1,1,2] → 频数总和 3；[] → 总和 0
    边界: 空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def plot_scatter(x: Sequence, y: Sequence) -> tuple[Figure, Axes]:
    """04. Scatter Plot
    Difficulty: Easy
    知识点: Figure, Axes, labels

    绘制散点图，设置标题、x/y 标签。 返回 (fig,ax)，不调用 show()。

    示例: [1,2],[3,4] → 两点；[],[] → 零点
    边界: 空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def plot_box(data: Sequence[Sequence[float]]) -> tuple[Figure, Axes]:
    """05. Box Plot
    Difficulty: Easy
    知识点: Figure, Axes, labels

    每个内部序列画一个箱体，使用 patch_artist=True，设置标题、x/y 标签；空外层不创建箱体。 返回 (fig,ax)，不调用 show()。

    示例: [[1,2],[3,4]] → 两个箱体；[] → 零箱体
    边界: 空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
