# Section 07 · Heap / Priority Queue

## 数据结构

二叉堆维护优先级顺序，使当前最高优先级的项目可以直接由堆顶读取。Python 标准库 `heapq` 支持最小堆。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 建堆、查看堆顶、入堆和弹出堆顶。 |
| 时间复杂度 | 对 `n` 个元素建堆为 `O(n)`，查看堆顶为 `O(1)`，入堆或弹出为 `O(log n)`。 |
| 空间复杂度 | 包含 `n` 个元素的堆占 `O(n)` 空间，定长 `k` 的堆占 `O(k)`。 |
| 常见使用场景 | 维护 Top K、流式统计、按优先级分配资源。 |

## 核心知识点

练习给元素定义优先级、固定堆容量、处理相同优先级，以及在多个堆之间维护平衡。

## 题目

本节共 10 题。子方向对应 YAML 中的 `subsection`。

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 703 | [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Easy | Top K | 数据流、定长堆、第 K 大元素 | [.py](easy/p0703_kth_largest_element_in_a_stream.py) |
| 1046 | [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | Easy | Priority Simulation | 最大优先级、碰撞后更新 | [.py](easy/p1046_last_stone_weight.py) |
| 2558 | [Take Gifts From the Richest Pile](https://leetcode.com/problems/take-gifts-from-the-richest-pile/) | Easy | Priority Simulation | 最大优先级、重复更新 | [.py](easy/p2558_take_gifts_from_the_richest_pile.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Top K | 堆容量、第 K 大元素 | [.py](medium/p0215_kth_largest_element_in_an_array.py) |
| 973 | [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Top K | 距离优先级、定长堆 | [.py](medium/p0973_k_closest_points_to_origin.py) |
| 1845 | [Seat Reservation Manager](https://leetcode.com/problems/seat-reservation-manager/) | Medium | Priority Simulation | 最小编号分配、回收 | [.py](medium/p1845_seat_reservation_manager.py) |
| 1642 | [Furthest Building You Can Reach](https://leetcode.com/problems/furthest-building-you-can-reach/) | Medium | Resource Allocation | 资源分配、堆顶替换 | [.py](medium/p1642_furthest_building_you_can_reach.py) |
| 2462 | [Total Cost to Hire K Workers](https://leetcode.com/problems/total-cost-to-hire-k-workers/) | Medium | Resource Allocation | 双候选范围、代价与索引优先级 | [.py](medium/p2462_total_cost_to_hire_k_workers.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 295 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | Streaming Statistics | 双堆、大小与顺序平衡 | [.py](hard/p0295_find_median_from_data_stream.py) |
| 871 | [Minimum Number of Refueling Stops](https://leetcode.com/problems/minimum-number-of-refueling-stops/) | Hard | Resource Allocation | 可用燃料、补给优先级 | [.py](hard/p0871_minimum_number_of_refueling_stops.py) |
