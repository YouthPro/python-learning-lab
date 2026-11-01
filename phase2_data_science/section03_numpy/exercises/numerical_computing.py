from __future__ import annotations

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """12. Cosine Similarity
    Difficulty: Medium
    知识点: dot, norm

    沿最后一维求余弦相似度，支持广播。Shape (...,D),(...,D) → (...)；两个 1D 输入可返回标量。零向量相似度定义为 0。

    示例: [1,0],[1,0] → 1；[0,0],[1,0] → 0
    边界: 零长度特征向量返回 0；避免除零警告。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """13. Stable Softmax
    Difficulty: Medium
    知识点: exp, max, sum

    先减去指定轴最大值再计算 softmax，Shape 保持不变。

    示例: [1000,1000] → [.5,.5]；[[0,0]],axis=1 → [[.5,.5]]
    边界: 空数组保持 shape；输入为有限数值，结果每条归约轴之和为 1。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def sample_data(seed: int, size: int | tuple[int, ...]) -> np.ndarray:
    """14. Reproducible Random Sampling
    Difficulty: Medium
    知识点: default_rng

    使用局部 default_rng(seed) 生成标准正态样本，不改变全局随机状态。Shape 由 size 决定。

    示例: seed=42,size=3 → 与 default_rng(42).standard_normal(3) 相同；size=0 → (0,)
    边界: 负 size 抛 ValueError；支持二维 size。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def batch_matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """15. Batch Matrix Multiplication
    Difficulty: Medium
    知识点: matmul

    批量矩阵乘法，Shape (...,M,K) @ (...,K,N) → (...,M,N)，batch 维可广播。

    示例: (2,3)@(3,4) → (2,4)；(2,1,3)@(3,4) → (2,1,4)
    边界: K 不一致抛 ValueError；支持零行和三维。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
