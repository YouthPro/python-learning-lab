from __future__ import annotations

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """04. Regression Metrics
    Difficulty: Medium
    知识点: MAE, MSE, R2

    返回 mae、mse、r2 三个 Python float；采用 sklearn.metrics 定义。

    示例: [1,2],[1,2] → {mae:0,mse:0,r2:1}；[0,2],[1,1] → {mae:1,mse:1,r2:0}
    边界: 至少两个样本；空输入抛 ValueError；常量目标遵循 force_finite 默认语义。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """05. Classification Metrics
    Difficulty: Medium
    知识点: accuracy, precision, recall, F1

    二分类标签 0/1，返回 accuracy、precision、recall、f1；precision/recall/f1 使用 zero_division=0。

    示例: [0,1],[0,1] → 全 1；[0,0],[0,0] → accuracy=1，其余 0
    边界: 空输入抛 ValueError；此题仅二分类。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[Figure, Axes]:
    """06. Confusion Matrix
    Difficulty: Medium
    知识点: ConfusionMatrixDisplay

    固定标签顺序 [0,1]，绘制 2×2 混淆矩阵并设置标题，返回 fig,ax。

    示例: [0,1],[0,1] → 单位对角计数；全 0 → 右下角 0
    边界: 即使只出现一个类别也必须有两个标签；不 show。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
