# Section 12 · Union-Find

## 数据结构

并查集（Disjoint Set Union）维护互不重叠的连通分量，内部状态通常包含父节点及集合大小或秩。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 初始化、查找代表元、合并、判断连通性和维护分量数量。 |
| 时间复杂度 | 初始化 `n` 个元素为 `O(n)`。同时使用路径压缩与按秩或大小合并时，查找和合并的均摊代价为 `O(α(n))`，其中 `α` 是反阿克曼函数。 |
| 空间复杂度 | 父节点、秩或大小共占 `O(n)` 空间。边和网格的输入规模单独计入。 |
| 常见使用场景 | 增量连通性、冗余边检测、网格分区和约束归并。 |

## 核心知识点

练习将元素映射为整数编号、让并查集表达等价关系，以及用分量代表元解释连通结果。

## 题目

本节共 11 题。子方向对应 YAML 中的 `subsection`。

### Easy

本级收录 0 题。

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 547 | [Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | Medium | Connectivity | 邻接矩阵、连通分量计数 | [.py](medium/p0547_number_of_provinces.py) |
| 684 | [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Medium | Connectivity | 逐边合并、冗余连接 | [.py](medium/p0684_redundant_connection.py) |
| 990 | [Satisfiability of Equality Equations](https://leetcode.com/problems/satisfiability-of-equality-equations/) | Medium | Constraints | 等式的连通关系与不等式检查 | [.py](medium/p0990_satisfiability_of_equality_equations.py) |
| 1319 | [Number of Operations to Make Network Connected](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) | Medium | Connectivity | 连通分量、冗余连接与可用操作数 | [.py](medium/p1319_number_of_operations_to_make_network_connected.py) |
| 785 | [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) | Medium | Constraints | 二分约束、顶点的同侧关系 | [.py](medium/p0785_is_graph_bipartite.py) |
| 959 | [Regions Cut By Slashes](https://leetcode.com/problems/regions-cut-by-slashes/) | Medium | Grid Connectivity | 单元格分区编号、并查集合并 | [.py](medium/p0959_regions_cut_by_slashes.py) |
| 947 | [Most Stones Removed with Same Row or Column](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/) | Medium | Connectivity | 行列坐标直接编号、编号域分离与并查集 | [.py](medium/p0947_most_stones_removed_with_same_row_or_column.py) |
| 1631 | [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | Medium | Edge Ordering | 边权排序、并查集连通性 | [.py](medium/p1631_path_with_minimum_effort.py) |
| 200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | Grid Connectivity | 网格坐标编号、并查集分量计数 | [.py](medium/p0200_number_of_islands.py) |
| 130 | [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | Medium | Grid Connectivity | 网格连通性、并查集的边界代表元 | [.py](medium/p0130_surrounded_regions.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 765 | [Couples Holding Hands](https://leetcode.com/problems/couples-holding-hands/) | Hard | Constraints | 情侣编号与连通分量 | [.py](hard/p0765_couples_holding_hands.py) |
