# Section 03: NumPy & Numerical Computing

## 学习目标

理解 ndarray、shape、axis、broadcasting 与 vectorization，并能进行数值计算。 学习者已掌握基础语法；本节不重复讲变量、循环与条件判断。

## 知识点

dtype、索引切片、广播、归约、归一化、随机生成器、稳定 softmax、矩阵乘法与梯度。

## 推荐学习顺序

先读 [题目目录](exercise_catalog.md)，按 array_operations → broadcasting → numerical_computing 的顺序完成练习；每题先理解边界契约，再写代码并运行对应测试。最后完成/阅读项目并在小数据上独立解释输出。

```bash
python -m pytest phase2_data_science/section03_numpy/tests -q
python -m pytest phase2_data_science/section03_numpy -q
python -m pytest phase2_data_science/section03_numpy/tests --strict-exercises -q
```

未修改的 TODO 默认显示 xfail；实现后断言会正常执行，错误实现会失败。严格模式中所有 TODO 都失败。默认通过不代表练习已完成。浮点结果使用 allclose 或 approx，随机样例固定种子。

## 练习与进度

- [ ] Exercise 01: [Array Constructor](exercise_catalog.md#01-array-constructor) — `create_array`
- [ ] Exercise 02: [Shape Transformer](exercise_catalog.md#02-shape-transformer) — `transform_shape`
- [ ] Exercise 03: [Matrix Slicing](exercise_catalog.md#03-matrix-slicing) — `slice_matrix`
- [ ] Exercise 04: [Boolean Filtering](exercise_catalog.md#04-boolean-filtering) — `filter_array`
- [ ] Exercise 05: [Axis Statistics](exercise_catalog.md#05-axis-statistics) — `axis_statistics`
- [ ] Exercise 06: [Array Concatenation](exercise_catalog.md#06-array-concatenation) — `combine_arrays`
- [ ] Exercise 07: [Normalize Array](exercise_catalog.md#07-normalize-array) — `normalize_array`
- [ ] Exercise 08: [One-Hot Encoding](exercise_catalog.md#08-one-hot-encoding) — `one_hot_encode`
- [ ] Exercise 09: [Batch Normalization](exercise_catalog.md#09-batch-normalization) — `normalize_batch`
- [ ] Exercise 10: [Pairwise Distance](exercise_catalog.md#10-pairwise-distance) — `pairwise_distance`
- [ ] Exercise 11: [Vectorized Clipping](exercise_catalog.md#11-vectorized-clipping) — `clip_values`
- [ ] Exercise 12: [Cosine Similarity](exercise_catalog.md#12-cosine-similarity) — `cosine_similarity`
- [ ] Exercise 13: [Stable Softmax](exercise_catalog.md#13-stable-softmax) — `softmax`
- [ ] Exercise 14: [Reproducible Random Sampling](exercise_catalog.md#14-reproducible-random-sampling) — `sample_data`
- [ ] Exercise 15: [Batch Matrix Multiplication](exercise_catalog.md#15-batch-matrix-multiplication) — `batch_matmul`

## 项目与进度

- [ ] [Image Processor](projects/image_processor/README.md)
- [ ] [Vector Similarity Engine](projects/vector_similarity/README.md)
- [ ] [Linear Regression From Scratch](projects/linear_regression/README.md)

## 完成标准

全部 15 道契约测试在严格模式通过；能解释数据结构选择、时间/空间开销和边界处理；项目满足各自 README 中的验收标准并产出报告。NumPy 练习优先使用向量化，避免逐元素 Python 循环；图形练习返回 Figure/Axes，不调用 show。

## 官方参考资料与练习平台

- [NumPy 官方入门](https://numpy.org/doc/stable/user/absolute_beginners.html)
