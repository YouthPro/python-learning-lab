from __future__ import annotations

import numpy as np


def normalize_batch(x: np.ndarray) -> np.ndarray:
    """09. Batch Normalization
    Difficulty: Medium
    知识点: broadcasting, axis

    沿 axis=0 标准化每个特征，使用总体标准差 ddof=0；零标准差特征输出 0。Shape (N,D) 或 (N,T,D) → 相同 shape。

    示例: [[1,2],[3,2]] → [[-1,0],[1,0]]；单样本 → 全零
    边界: 空 batch 原样 shape 返回；只处理有限浮点数。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def pairwise_distance(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """10. Pairwise Distance
    Difficulty: Medium
    知识点: broadcasting, norm

    计算欧氏距离。Shape: (...,N,D),(...,M,D) → (...,N,M)，前导 batch 维遵循广播。

    示例: [[0,0]],[[3,4]] → [[5]]；(0,2),(3,2) → (0,3)
    边界: 支持二维与三维；特征数不相等抛 ValueError。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def clip_values(arr: np.ndarray, low: float, high: float) -> np.ndarray:
    """11. Vectorized Clipping
    Difficulty: Medium
    知识点: vectorization, clip

    将每个元素限制到闭区间 [low,high]，返回新数组；Shape 不变。

    示例: [-1,2,8],0,5 → [0,2,5]；[],0,1 → []
    边界: low>high 抛 ValueError；支持多维。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
