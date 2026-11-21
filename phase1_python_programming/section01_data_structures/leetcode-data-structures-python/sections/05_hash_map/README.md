# Section 05 · HashMap

## 数据结构

哈希表以键定位值。Python 的 `dict` 适合保存频次、位置和双向映射。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 检查键、读取、插入、覆盖和删除。 |
| 时间复杂度 | 常用的查找、插入和删除平均为 `O(1)`。长键的哈希和比较开销需要单独计入，严重冲突时单次操作最多为 `O(n)`。 |
| 空间复杂度 | `n` 个条目使用 `O(n)` 表空间。值中的分组内容另计。 |
| 常见使用场景 | 计数、按键查找、分组和维护窗口内统计。 |

## 核心知识点

练习设计键、处理缺失键、维护双向对应、给字典计数赋予区间含义。

## 题目

本节共 10 题。子方向对应 YAML 中的 `subsection`。

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Lookup | 值到索引的映射、补数查找 | [.py](easy/p0001_two_sum.py) |
| 205 | [Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/) | Easy | Mapping | 字符映射、一一对应 | [.py](easy/p0205_isomorphic_strings.py) |
| 290 | [Word Pattern](https://leetcode.com/problems/word-pattern/) | Easy | Mapping | 词与模式的位置对应、双向映射 | [.py](easy/p0290_word_pattern.py) |
| 242 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Easy | Frequency Counting | 字符频次、计数比较 | [.py](easy/p0242_valid_anagram.py) |
| 383 | [Ransom Note](https://leetcode.com/problems/ransom-note/) | Easy | Frequency Counting | 字符库存、计数扣减 | [.py](easy/p0383_ransom_note.py) |
| 387 | [First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/) | Easy | Frequency Counting | 出现次数、保留初始位置 | [.py](easy/p0387_first_unique_character_in_a_string.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Grouping | 分组键、结果分组 | [.py](medium/p0049_group_anagrams.py) |
| 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Prefix Sums | 运行中的前缀和、频次映射 | [.py](medium/p0560_subarray_sum_equals_k.py) |
| 454 | [4Sum II](https://leetcode.com/problems/4sum-ii/) | Medium | Frequency Counting | 组合和、计数映射 | [.py](medium/p0454_4sum_ii.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 76 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | Sliding Window | 窗口内字符频次、覆盖条件 | [.py](hard/p0076_minimum_window_substring.py) |
