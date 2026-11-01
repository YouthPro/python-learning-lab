# Section 03 练习题目录

约定优先于习惯性题解：按这里的排序、返回类型、缺失值和边界行为实现。

## 01. Array Constructor

- 难度：Medium
- 知识点：array, dtype
- 文件：[exercises/array_operations.py](exercises/array_operations.py)

```python
def create_array(data: list) -> np.ndarray
```

将矩形数值序列转换成独立的 float64 ndarray。Shape: (N,) 或 (N,D) → 相同 shape。

输入输出示例：[1,2] → float64 [1,2]；[] → shape (0,)

边界条件：支持二维、空数组；不允许 object 数组。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 02. Shape Transformer

- 难度：Medium
- 知识点：reshape
- 文件：[exercises/array_operations.py](exercises/array_operations.py)

```python
def transform_shape(arr: np.ndarray, shape: tuple[int, ...]) -> np.ndarray
```

按 C 顺序 reshape；Shape: 任意 → shape；允许一个 -1 推断。

输入输出示例：arange(6),(2,3) → [[0,1,2],[3,4,5]]；空数组,(0,2) → (0,2)

边界条件：元素数不匹配抛 ValueError。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 03. Matrix Slicing

- 难度：Medium
- 知识点：indexing
- 文件：[exercises/array_operations.py](exercises/array_operations.py)

```python
def slice_matrix(arr: np.ndarray, rows: slice, cols: slice) -> np.ndarray
```

对二维数组执行行列切片，返回所选矩形。Shape: (N,D) → (R,C)。

输入输出示例：arange(9).reshape(3,3),slice(1,3),slice(0,2) → [[3,4],[6,7]]；零行切片 → (0,C)

边界条件：支持步长和负索引。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 04. Boolean Filtering

- 难度：Medium
- 知识点：boolean indexing
- 文件：[exercises/array_operations.py](exercises/array_operations.py)

```python
def filter_array(arr: np.ndarray, condition: np.ndarray) -> np.ndarray
```

布尔掩码与 arr 形状相同，返回所有为 True 的元素，按 C 顺序展开为一维。Shape: (...) → (K,)。

输入输出示例：[1,2],[True,False] → [1]；二维对角掩码 → 对角元素

边界条件：空输入返回 shape (0,)；形状不匹配抛 IndexError 或 ValueError。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 05. Axis Statistics

- 难度：Medium
- 知识点：sum, mean, max, axis
- 文件：[exercises/array_operations.py](exercises/array_operations.py)

```python
def axis_statistics(arr: np.ndarray, axis: int) -> dict[str, np.ndarray]
```

沿 axis 返回 {sum,mean,max}；Shape: (d0,…,dn) → 每项去掉 axis 维。

输入输出示例：[[1,3],[5,7]],axis=0 → sum [6,10],mean [3,5],max [5,7]；axis=1 → sum [4,12]

边界条件：被归约的轴长度为 0 时抛 ValueError；支持负 axis。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 06. Array Concatenation

- 难度：Medium
- 知识点：concatenate, stack
- 文件：[exercises/array_operations.py](exercises/array_operations.py)

```python
def combine_arrays(a: np.ndarray, b: np.ndarray, axis: int) -> np.ndarray
```

沿已有 axis 拼接，其他维度必须一致。Shape: (N,D)+(M,D),axis=0 → (N+M,D)。可另练 stack，主函数按 concatenate。

输入输出示例：[1],[2],0 → [1,2]；(0,2)+(1,2),0 → (1,2)

边界条件：不相容 shape 抛 ValueError；支持负 axis。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 07. Normalize Array

- 难度：Medium
- 知识点：broadcasting, min-max
- 文件：[exercises/array_operations.py](exercises/array_operations.py)

```python
def normalize_array(arr: np.ndarray) -> np.ndarray
```

对全数组 min-max 归一化到 [0,1]，返回浮点数组；常量数组返回全零。Shape 保持不变。

输入输出示例：[2,4,6] → [0,.5,1]；[7,7] → [0,0]

边界条件：空数组保持 shape；输入不含 NaN/Inf；不修改原数组。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 08. One-Hot Encoding

- 难度：Medium
- 知识点：advanced indexing
- 文件：[exercises/array_operations.py](exercises/array_operations.py)

```python
def one_hot_encode(labels: np.ndarray, num_classes: int) -> np.ndarray
```

整数 labels Shape (N,) → 整数 one-hot (N,C)。

输入输出示例：[0,2],3 → [[1,0,0],[0,0,1]]；[],2 → (0,2)

边界条件：C>0；标签必须 0≤label<C；否则 ValueError。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 09. Batch Normalization

- 难度：Medium
- 知识点：broadcasting, axis
- 文件：[exercises/broadcasting.py](exercises/broadcasting.py)

```python
def normalize_batch(x: np.ndarray) -> np.ndarray
```

沿 axis=0 标准化每个特征，使用总体标准差 ddof=0；零标准差特征输出 0。Shape (N,D) 或 (N,T,D) → 相同 shape。

输入输出示例：[[1,2],[3,2]] → [[-1,0],[1,0]]；单样本 → 全零

边界条件：空 batch 原样 shape 返回；只处理有限浮点数。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 10. Pairwise Distance

- 难度：Medium
- 知识点：broadcasting, norm
- 文件：[exercises/broadcasting.py](exercises/broadcasting.py)

```python
def pairwise_distance(x: np.ndarray, y: np.ndarray) -> np.ndarray
```

计算欧氏距离。Shape: (...,N,D),(...,M,D) → (...,N,M)，前导 batch 维遵循广播。

输入输出示例：[[0,0]],[[3,4]] → [[5]]；(0,2),(3,2) → (0,3)

边界条件：支持二维与三维；特征数不相等抛 ValueError。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 11. Vectorized Clipping

- 难度：Medium
- 知识点：vectorization, clip
- 文件：[exercises/broadcasting.py](exercises/broadcasting.py)

```python
def clip_values(arr: np.ndarray, low: float, high: float) -> np.ndarray
```

将每个元素限制到闭区间 [low,high]，返回新数组；Shape 不变。

输入输出示例：[-1,2,8],0,5 → [0,2,5]；[],0,1 → []

边界条件：low>high 抛 ValueError；支持多维。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 12. Cosine Similarity

- 难度：Medium
- 知识点：dot, norm
- 文件：[exercises/numerical_computing.py](exercises/numerical_computing.py)

```python
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray
```

沿最后一维求余弦相似度，支持广播。Shape (...,D),(...,D) → (...)；两个 1D 输入可返回标量。零向量相似度定义为 0。

输入输出示例：[1,0],[1,0] → 1；[0,0],[1,0] → 0

边界条件：零长度特征向量返回 0；避免除零警告。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 13. Stable Softmax

- 难度：Medium
- 知识点：exp, max, sum
- 文件：[exercises/numerical_computing.py](exercises/numerical_computing.py)

```python
def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray
```

先减去指定轴最大值再计算 softmax，Shape 保持不变。

输入输出示例：[1000,1000] → [.5,.5]；[[0,0]],axis=1 → [[.5,.5]]

边界条件：空数组保持 shape；输入为有限数值，结果每条归约轴之和为 1。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 14. Reproducible Random Sampling

- 难度：Medium
- 知识点：default_rng
- 文件：[exercises/numerical_computing.py](exercises/numerical_computing.py)

```python
def sample_data(seed: int, size: int | tuple[int, ...]) -> np.ndarray
```

使用局部 default_rng(seed) 生成标准正态样本，不改变全局随机状态。Shape 由 size 决定。

输入输出示例：seed=42,size=3 → 与 default_rng(42).standard_normal(3) 相同；size=0 → (0,)

边界条件：负 size 抛 ValueError；支持二维 size。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 15. Batch Matrix Multiplication

- 难度：Medium
- 知识点：matmul
- 文件：[exercises/numerical_computing.py](exercises/numerical_computing.py)

```python
def batch_matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray
```

批量矩阵乘法，Shape (...,M,K) @ (...,K,N) → (...,M,N)，batch 维可广播。

输入输出示例：(2,3)@(3,4) → (2,4)；(2,1,3)@(3,4) → (2,1,4)

边界条件：K 不一致抛 ValueError；支持零行和三维。

提示：先运行对应测试，理解返回结构，再查官方文档。
