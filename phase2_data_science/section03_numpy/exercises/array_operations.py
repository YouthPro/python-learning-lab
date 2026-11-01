from __future__ import annotations

import numpy as np


def create_array(data: list) -> np.ndarray:
    """01. Array Constructor
    Difficulty: Medium
    知识点: array, dtype

    将矩形数值序列转换成独立的 float64 ndarray。Shape: (N,) 或 (N,D) → 相同 shape。

    示例: [1,2] → float64 [1,2]；[] → shape (0,)
    边界: 支持二维、空数组；不允许 object 数组。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def transform_shape(arr: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    """02. Shape Transformer
    Difficulty: Medium
    知识点: reshape

    按 C 顺序 reshape；Shape: 任意 → shape；允许一个 -1 推断。

    示例: arange(6),(2,3) → [[0,1,2],[3,4,5]]；空数组,(0,2) → (0,2)
    边界: 元素数不匹配抛 ValueError。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def slice_matrix(arr: np.ndarray, rows: slice, cols: slice) -> np.ndarray:
    """03. Matrix Slicing
    Difficulty: Medium
    知识点: indexing

    对二维数组执行行列切片，返回所选矩形。Shape: (N,D) → (R,C)。

    示例: arange(9).reshape(3,3),slice(1,3),slice(0,2) → [[3,4],[6,7]]；零行切片 → (0,C)
    边界: 支持步长和负索引。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def filter_array(arr: np.ndarray, condition: np.ndarray) -> np.ndarray:
    """04. Boolean Filtering
    Difficulty: Medium
    知识点: boolean indexing

    布尔掩码与 arr 形状相同，返回所有为 True 的元素，按 C 顺序展开为一维。Shape: (...) → (K,)。

    示例: [1,2],[True,False] → [1]；二维对角掩码 → 对角元素
    边界: 空输入返回 shape (0,)；形状不匹配抛 IndexError 或 ValueError。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def axis_statistics(arr: np.ndarray, axis: int) -> dict[str, np.ndarray]:
    """05. Axis Statistics
    Difficulty: Medium
    知识点: sum, mean, max, axis

    沿 axis 返回 {sum,mean,max}；Shape: (d0,…,dn) → 每项去掉 axis 维。

    示例: [[1,3],[5,7]],axis=0 → sum [6,10],mean [3,5],max [5,7]；axis=1 → sum [4,12]
    边界: 被归约的轴长度为 0 时抛 ValueError；支持负 axis。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def combine_arrays(a: np.ndarray, b: np.ndarray, axis: int) -> np.ndarray:
    """06. Array Concatenation
    Difficulty: Medium
    知识点: concatenate, stack

    沿已有 axis 拼接，其他维度必须一致。Shape: (N,D)+(M,D),axis=0 → (N+M,D)。可另练 stack，主函数按 concatenate。

    示例: [1],[2],0 → [1,2]；(0,2)+(1,2),0 → (1,2)
    边界: 不相容 shape 抛 ValueError；支持负 axis。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def normalize_array(arr: np.ndarray) -> np.ndarray:
    """07. Normalize Array
    Difficulty: Medium
    知识点: broadcasting, min-max

    对全数组 min-max 归一化到 [0,1]，返回浮点数组；常量数组返回全零。Shape 保持不变。

    示例: [2,4,6] → [0,.5,1]；[7,7] → [0,0]
    边界: 空数组保持 shape；输入不含 NaN/Inf；不修改原数组。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def one_hot_encode(labels: np.ndarray, num_classes: int) -> np.ndarray:
    """08. One-Hot Encoding
    Difficulty: Medium
    知识点: advanced indexing

    整数 labels Shape (N,) → 整数 one-hot (N,C)。

    示例: [0,2],3 → [[1,0,0],[0,0,1]]；[],2 → (0,2)
    边界: C>0；标签必须 0≤label<C；否则 ValueError。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
