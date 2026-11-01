from __future__ import annotations

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def split_dataset(X: np.ndarray, y: np.ndarray, random_state: int = 42) -> tuple:
    """01. Train Test Split
    Difficulty: Medium
    知识点: train_test_split

    按 test_size=0.2、shuffle=True 划分；返回 X_train,X_test,y_train,y_test；random_state 可配置。

    示例: 10 行 → 8 训练/2 测试；5 行 → 4/1
    边界: 空输入抛 ValueError；相同种子结果一致。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def scale_features(X: np.ndarray) -> tuple[np.ndarray, StandardScaler]:
    """02. Feature Scaling
    Difficulty: Medium
    知识点: StandardScaler

    仅把传入的训练矩阵进行 fit_transform，返回 (scaled,scaler)；未来测试集必须用此 scaler.transform。

    示例: [[1],[3]] → [[-1],[1]]；常量列 → 全零
    边界: 空训练输入抛 ValueError；使用 ddof=0。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def build_preprocessing_pipeline() -> Pipeline:
    """03. Missing Value Pipeline
    Difficulty: Medium
    知识点: SimpleImputer, Pipeline

    返回未拟合 Pipeline，命名步骤 imputer（median、keep_empty_features=True）与 scaler（StandardScaler）；每次调用返回独立实例。

    示例: [[1],[NaN],[3]] → 填 2 再标准化；全缺失列 → 填 0
    边界: 不能在构建函数内拟合；交叉验证时将完整预处理放进模型 Pipeline。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
