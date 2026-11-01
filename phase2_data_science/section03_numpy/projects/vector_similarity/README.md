# Vector Similarity Engine

## 项目目标与需求

实现欧氏距离、曼哈顿距离、余弦相似度、批查询、全相似度矩阵与 Top K，比较循环和向量化耗时。

## 输入数据

vectors 为 (...,N,D)，queries 为 (...,Q,D) 或单向量 (D,)；支持二维和三维 batch 广播，零向量余弦定义为 0。

## 文件结构

src/vector_similarity.py：normalize_vectors、pairwise、top_k、benchmark、main。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase2_data_science.section03_numpy.projects.vector_similarity.src.vector_similarity --input datasets/generated/vectors.npy --k 5 --output datasets/processed/vector_similarity.json
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

JSON 包含 Top K 索引和分数以及两种实现的耗时。pairwise 输出 (...,Q,N)，cosine 越大越相似，其余距离越小越相似。

## 验收标准

Top K 并列按原索引；k 大于 N 时截到 N；空输入支持；检索按 query 分块控制临时矩阵（Manhattan 临时空间 O(chunk×N×D)）。完整矩阵仍需 O(Q×N) 输出空间。

```bash
python -m pytest phase2_data_science/section03_numpy/projects/vector_similarity/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
