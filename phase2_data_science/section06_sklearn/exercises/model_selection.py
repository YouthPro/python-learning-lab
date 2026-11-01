from __future__ import annotations

import numpy as np
from sklearn.model_selection import GridSearchCV


def evaluate_cv(model, X: np.ndarray, y: np.ndarray, random_state: int = 42) -> np.ndarray:
    """07. Cross Validation
    Difficulty: Medium
    知识点: cross_val_score, KFold

    使用 KFold(n_splits=3,shuffle=True,random_state=...) 和 scoring=r2 返回三折分数；传入完整回归 Pipeline 以避免泄漏。

    示例: 线性数据+LinearRegression → 三个 1；噪声数据 → 三个分数
    边界: 至少 3 行；不拟合调用方模型，固定划分。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def search_best_params(
    model, params: dict, X: np.ndarray, y: np.ndarray, random_state: int = 42
) -> GridSearchCV:
    """08. Hyperparameter Search
    Difficulty: Medium
    知识点: GridSearchCV

    以相同三折 KFold、scoring=r2、refit=True 拟合 GridSearchCV，返回搜索对象；参数名支持 Pipeline 的 step__param。

    示例: Ridge,alpha=[.1,1] → fitted search；单候选 → 一个结果
    边界: 只传训练数据；error_score=raise，空参数字典合法。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
