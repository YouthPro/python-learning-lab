# Section 01 · Array

## 数据结构

Python 的 `list` 用动态数组按顺序存放元素，支持通过索引访问和更新位置。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 索引读写、尾部追加、原地交换、顺序扫描。 |
| 时间复杂度 | 索引读写 `O(1)`，尾部追加均摊 `O(1)`，中间插入或删除 `O(n)`。 |
| 空间复杂度 | 存储 `n` 个元素需要 `O(n)` 空间。单次原地扫描常用 `O(1)` 额外空间。 |
| 常见使用场景 | 有序序列合并、区间扫描、原地重排和按位置访问。 |

## 核心知识点

练习有效区间、读写指针、累积状态和二分边界。记录操作是否要求保留元素的相对顺序。

## 题目

本节共 13 题。子方向对应 YAML 中的 `subsection`。

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 26 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Easy | Array Manipulation | 有序数组、原地去重与写入位置 | [.py](easy/p0026_remove_duplicates_from_sorted_array.py) |
| 27 | [Remove Element](https://leetcode.com/problems/remove-element/) | Easy | Array Manipulation | 原地写入、有效长度 | [.py](easy/p0027_remove_element.py) |
| 88 | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | Easy | Array Manipulation | 有序数组合并、尾部容量 | [.py](easy/p0088_merge_sorted_array.py) |
| 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Linear Scan | 扫描区间、运行中的最小值 | [.py](easy/p0121_best_time_to_buy_and_sell_stock.py) |
| 283 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Easy | Array Manipulation | 原地移动、相对顺序 | [.py](easy/p0283_move_zeroes.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 53 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | Linear Scan | 连续子数组、区间状态 | [.py](medium/p0053_maximum_subarray.py) |
| 11 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Two Pointers | 左右端点、跨度和高度 | [.py](medium/p0011_container_with_most_water.py) |
| 75 | [Sort Colors](https://leetcode.com/problems/sort-colors/) | Medium | Array Manipulation | 原地分区、下标不变量 | [.py](medium/p0075_sort_colors.py) |
| 15 | [3Sum](https://leetcode.com/problems/3sum/) | Medium | Two Pointers | 排序、双指针、去重 | [.py](medium/p0015_3sum.py) |
| 238 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Prefix and Suffix | 前缀积、后缀积、输出空间复用 | [.py](medium/p0238_product_of_array_except_self.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 42 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Two Pointers | 双指针、左右边界高度 | [.py](hard/p0042_trapping_rain_water.py) |
| 41 | [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | Hard | Array Manipulation | 值与下标的对应、原地置换 | [.py](hard/p0041_first_missing_positive.py) |
| 4 | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | Binary Search | 两个有序数组的分割位置和二分边界 | [.py](hard/p0004_median_of_two_sorted_arrays.py) |
