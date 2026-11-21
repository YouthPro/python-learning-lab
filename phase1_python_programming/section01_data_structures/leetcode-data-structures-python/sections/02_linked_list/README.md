# Section 02 · Linked List

## 数据结构

单链表的节点保存一个值和指向后继的引用，从头节点沿 `next` 逐项访问。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 遍历、插入、摘除、断开和重连节点。 |
| 时间复杂度 | 查找和遍历为 `O(n)`。已定位到前驱时，插入和摘除单个节点为 `O(1)`。 |
| 空间复杂度 | 节点占 `O(n)` 空间。迭代方式重连节点通常只需 `O(1)` 额外空间，递归时另计调用栈。 |
| 常见使用场景 | 局部插入和删除、顺序合并、原地调整一段链。 |

## 核心知识点

练习节点身份、前驱与后继、快慢指针、哑节点以及首尾边界。

## 题目

本节共 15 题。子方向对应 YAML 中的 `subsection`。

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | Pointer Manipulation | 前驱、当前节点、后继的引用关系 | [.py](easy/p0206_reverse_linked_list.py) |
| 21 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Merge and Sort | 有序合并、节点复用 | [.py](easy/p0021_merge_two_sorted_lists.py) |
| 141 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy | Fast and Slow Pointers | 快慢指针、判环 | [.py](easy/p0141_linked_list_cycle.py) |
| 876 | [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | Easy | Fast and Slow Pointers | 快慢指针、中点边界 | [.py](easy/p0876_middle_of_the_linked_list.py) |
| 83 | [Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) | Easy | Pointer Manipulation | 相邻重复值、节点摘除 | [.py](easy/p0083_remove_duplicates_from_sorted_list.py) |
| 203 | [Remove Linked List Elements](https://leetcode.com/problems/remove-linked-list-elements/) | Easy | Pointer Manipulation | 哑节点、首节点删除 | [.py](easy/p0203_remove_linked_list_elements.py) |
| 160 | [Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/) | Easy | Pointer Manipulation | 指针同步、节点身份 | [.py](easy/p0160_intersection_of_two_linked_lists.py) |
| 234 | [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | Easy | Fast and Slow Pointers | 链表中点、反转与回文比较 | [.py](easy/p0234_palindrome_linked_list.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 19 | [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Fast and Slow Pointers | 指针间距、哑节点 | [.py](medium/p0019_remove_nth_node_from_end_of_list.py) |
| 24 | [Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) | Medium | Pointer Manipulation | 成对换链、相邻区间连接 | [.py](medium/p0024_swap_nodes_in_pairs.py) |
| 92 | [Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/) | Medium | Pointer Manipulation | 局部反转、区间边界 | [.py](medium/p0092_reverse_linked_list_ii.py) |
| 142 | [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | Medium | Fast and Slow Pointers | 快慢指针、环入口 | [.py](medium/p0142_linked_list_cycle_ii.py) |
| 143 | [Reorder List](https://leetcode.com/problems/reorder-list/) | Medium | Pointer Manipulation | 分段、反转与交错重连 | [.py](medium/p0143_reorder_list.py) |
| 148 | [Sort List](https://leetcode.com/problems/sort-list/) | Medium | Merge and Sort | 链表归并排序、分段与合并 | [.py](medium/p0148_sort_list.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 25 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Hard | Pointer Manipulation | 分组反转、完整组的边界 | [.py](hard/p0025_reverse_nodes_in_k_group.py) |
