# Section 06 · HashSet

## 数据结构

集合记录不同的可哈希元素。Python 的 `set` 提供成员测试和集合运算。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 添加、移除、成员测试、交集。 |
| 时间复杂度 | 常用的添加、移除和成员测试平均为 `O(1)`，严重冲突时单次操作最多为 `O(n)`。两集合交集通常按较小集合的大小计时。 |
| 空间复杂度 | 存下 `n` 个不同元素需要 `O(n)` 空间。 |
| 常见使用场景 | 去重、访问状态、约束冲突检测和快速成员判断。 |

## 核心知识点

练习选择可哈希的状态、识别重复或环、限定一次检查所涵盖的约束。

## 题目

本节共 10 题。子方向对应 YAML 中的 `subsection`。

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 217 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Easy | Membership | 成员测试、重复值 | [.py](easy/p0217_contains_duplicate.py) |
| 202 | [Happy Number](https://leetcode.com/problems/happy-number/) | Easy | State Tracking | 重复状态、环检测 | [.py](easy/p0202_happy_number.py) |
| 349 | [Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays/) | Easy | Membership | 交集、唯一性 | [.py](easy/p0349_intersection_of_two_arrays.py) |
| 771 | [Jewels and Stones](https://leetcode.com/problems/jewels-and-stones/) | Easy | Membership | 允许字符、成员判断 | [.py](easy/p0771_jewels_and_stones.py) |
| 804 | [Unique Morse Code Words](https://leetcode.com/problems/unique-morse-code-words/) | Easy | Deduplication | 编码结果、去重 | [.py](easy/p0804_unique_morse_code_words.py) |
| 705 | [Design HashSet](https://leetcode.com/problems/design-hashset/) | Easy | Set Design | 集合接口、键域与内部存储 | [.py](easy/p0705_design_hashset.py) |
| 2351 | [First Letter to Appear Twice](https://leetcode.com/problems/first-letter-to-appear-twice/) | Easy | State Tracking | 字符出现顺序、首次重复 | [.py](easy/p2351_first_letter_to_appear_twice.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 128 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | Membership | 连续段边界、整数成员测试 | [.py](medium/p0128_longest_consecutive_sequence.py) |
| 874 | [Walking Robot Simulation](https://leetcode.com/problems/walking-robot-simulation/) | Medium | State Tracking | 坐标键、障碍物成员测试 | [.py](medium/p0874_walking_robot_simulation.py) |
| 36 | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | Medium | Constraint Tracking | 行、列与宫内的唯一性 | [.py](medium/p0036_valid_sudoku.py) |

### Hard

本级收录 0 题。
