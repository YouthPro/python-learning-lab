# Section 08 · Binary Tree

## 数据结构

二叉树的每个节点至多有左右两个孩子。形状、递归次序和子树返回值决定可用的遍历方式。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 访问子节点、递归遍历、调整指针和组合子树结果。 |
| 时间复杂度 | 访问一个节点和更新一个指针为 `O(1)`。遍历所有 `n` 个节点为 `O(n)`。 |
| 空间复杂度 | 树节点占 `O(n)` 空间。高度为 `h` 的树递归需要 `O(h)` 调用栈，遍历结果单独计入输出空间。 |
| 常见使用场景 | 层级结构、整棵树的比较和变换、路径聚合和序列化。 |

## 核心知识点

练习先序、中序、后序的访问时机，空树基例，子树状态和递归 DFS。

## 题目

本节共 15 题。子方向对应 YAML 中的 `subsection`。

第 297 题显式列出官方示例调用的无参构造 `Codec()`，并为序列化和反序列化补充包含空树的类型注解。 [LeetCode 297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 144 | [Binary Tree Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/) | Easy | Traversal | 先序递归、根节点访问时机 | [.py](easy/p0144_binary_tree_preorder_traversal.py) |
| 94 | [Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) | Easy | Traversal | 中序递归、左右子树顺序 | [.py](easy/p0094_binary_tree_inorder_traversal.py) |
| 145 | [Binary Tree Postorder Traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/) | Easy | Traversal | 后序递归、子树返回后访问 | [.py](easy/p0145_binary_tree_postorder_traversal.py) |
| 100 | [Same Tree](https://leetcode.com/problems/same-tree/) | Easy | Tree Properties | 结构与节点值、空树比较 | [.py](easy/p0100_same_tree.py) |
| 104 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Easy | Tree Properties | 子树高度、递归基例 | [.py](easy/p0104_maximum_depth_of_binary_tree.py) |
| 226 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Easy | Tree Transformation | 左右子树、原地指针更新 | [.py](easy/p0226_invert_binary_tree.py) |
| 101 | [Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) | Easy | Tree Properties | 对称节点、镜像递归 | [.py](easy/p0101_symmetric_tree.py) |
| 112 | [Path Sum](https://leetcode.com/problems/path-sum/) | Easy | Path Tracking | 根到叶路径、路径状态 | [.py](easy/p0112_path_sum.py) |
| 110 | [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | Easy | Tree Properties | 高度差、子树平衡状态 | [.py](easy/p0110_balanced_binary_tree.py) |
| 543 | [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | Path Tracking | 树高、经过节点的路径长度 | [.py](easy/p0543_diameter_of_binary_tree.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 114 | [Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) | Medium | Tree Transformation | 先序顺序、树节点指针重连 | [.py](medium/p0114_flatten_binary_tree_to_linked_list.py) |
| 236 | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | Path Tracking | 最近公共祖先、子树匹配状态 | [.py](medium/p0236_lowest_common_ancestor_of_a_binary_tree.py) |
| 129 | [Sum Root to Leaf Numbers](https://leetcode.com/problems/sum-root-to-leaf-numbers/) | Medium | Path Tracking | 路径数字、逐层累积 | [.py](medium/p0129_sum_root_to_leaf_numbers.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 124 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | Path Tracking | 路径贡献、子树返回状态 | [.py](hard/p0124_binary_tree_maximum_path_sum.py) |
| 297 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | Serialization | 递归 DFS、空节点标记 | [.py](hard/p0297_serialize_and_deserialize_binary_tree.py) |
