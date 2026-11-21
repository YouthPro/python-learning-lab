# Section 09 · Binary Search Tree

## 数据结构

二叉搜索树（BST）按键的大小组织节点。典型的严格 BST 让左子树键小于根、右子树键大于根，中序遍历按有序顺序访问节点。重复值按具体题意处理。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 按键查找、插入、删除、范围查询和中序遍历。 |
| 时间复杂度 | 查找、插入和删除为 `O(h)`，`h` 是树高，中序遍历全部节点为 `O(n)`。平衡树的 `h` 为 `O(log n)`，退化时可达 `O(n)`。 |
| 空间复杂度 | 存储 `n` 个节点需要 `O(n)`。递归调用栈最多 `O(h)`。 |
| 常见使用场景 | 有序查找、范围裁剪、按序统计和动态维护键。 |

## 核心知识点

练习有序边界、子树剪枝、相邻键之间的关系，以及修改节点后的 BST 不变量。

## 题目

本节共 13 题。子方向对应 YAML 中的 `subsection`。

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 700 | [Search in a Binary Search Tree](https://leetcode.com/problems/search-in-a-binary-search-tree/) | Easy | Search and Range | 按比较结果选择子树 | [.py](easy/p0700_search_in_a_binary_search_tree.py) |
| 530 | [Minimum Absolute Difference in BST](https://leetcode.com/problems/minimum-absolute-difference-in-bst/) | Easy | Inorder Statistics | 有序访问、相邻键的最小差 | [.py](easy/p0530_minimum_absolute_difference_in_bst.py) |
| 501 | [Find Mode in Binary Search Tree](https://leetcode.com/problems/find-mode-in-binary-search-tree/) | Easy | Inorder Statistics | 中序遍历、相同值的连续计数 | [.py](easy/p0501_find_mode_in_binary_search_tree.py) |
| 783 | [Minimum Distance Between BST Nodes](https://leetcode.com/problems/minimum-distance-between-bst-nodes/) | Easy | Inorder Statistics | 中序相邻关系、最小键差 | [.py](easy/p0783_minimum_distance_between_bst_nodes.py) |
| 938 | [Range Sum of BST](https://leetcode.com/problems/range-sum-of-bst/) | Easy | Search and Range | 区间边界、BST 子树剪枝 | [.py](easy/p0938_range_sum_of_bst.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 98 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | BST Validation | 全局上下界、严格顺序 | [.py](medium/p0098_validate_binary_search_tree.py) |
| 230 | [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Medium | Inorder Statistics | 访问次序、第 K 小节点 | [.py](medium/p0230_kth_smallest_element_in_a_bst.py) |
| 235 | [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Medium | Search and Range | 目标值分岔位置、祖先范围 | [.py](medium/p0235_lowest_common_ancestor_of_a_binary_search_tree.py) |
| 450 | [Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/) | Medium | Tree Updates | 删除后的有序性、节点重连 | [.py](medium/p0450_delete_node_in_a_bst.py) |
| 701 | [Insert into a Binary Search Tree](https://leetcode.com/problems/insert-into-a-binary-search-tree/) | Medium | Tree Updates | 插入位置、子树引用 | [.py](medium/p0701_insert_into_a_binary_search_tree.py) |
| 669 | [Trim a Binary Search Tree](https://leetcode.com/problems/trim-a-binary-search-tree/) | Medium | Tree Updates | 保留区间、子树裁剪 | [.py](medium/p0669_trim_a_binary_search_tree.py) |
| 538 | [Convert BST to Greater Tree](https://leetcode.com/problems/convert-bst-to-greater-tree/) | Medium | Inorder Statistics | 逆序中序、运行累积量 | [.py](medium/p0538_convert_bst_to_greater_tree.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 1373 | [Maximum Sum BST in Binary Tree](https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/) | Hard | BST Validation | 后序状态、子树范围和键和 | [.py](hard/p1373_maximum_sum_bst_in_binary_tree.py) |
