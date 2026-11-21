# Section 10 · Trie

## 数据结构

Trie 用树路径表示字符或二进制位的前缀。多个键可以共享路径，节点可记录结束标记、计数等内部状态。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 按字符或位前进、插入键、匹配前缀、查询结束标记。 |
| 时间复杂度 | 给定固定字母表且能直接定位孩子时，长度 `L` 的插入和精确查询为 `O(L)`。通配符查询的代价取决于实际访问的节点数。 |
| 空间复杂度 | 固定字母表下，空间与不同前缀数成正比。二进制 Trie 的节点数受键数量和位宽限制。 |
| 常见使用场景 | 字典前缀查找、通配词检索、前缀计数和按位查询。 |

## 核心知识点

练习区分完整键和前缀，设计节点的计数与索引状态，并明确字符表或位宽。

## 题目

本节共 11 题。子方向对应 YAML 中的 `subsection`。

### Easy

本级收录 0 题。

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 208 | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Character Trie | 插入、完整词查找、前缀查找 | [.py](medium/p0208_implement_trie_prefix_tree.py) |
| 211 | [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Medium | Wildcard Search | 通配符、可达分支、结束标记 | [.py](medium/p0211_design_add_and_search_words_data_structure.py) |
| 648 | [Replace Words](https://leetcode.com/problems/replace-words/) | Medium | Character Trie | 词根前缀、词边界 | [.py](medium/p0648_replace_words.py) |
| 676 | [Implement Magic Dictionary](https://leetcode.com/problems/implement-magic-dictionary/) | Medium | Wildcard Search | 沿路径匹配、单字符差异 | [.py](medium/p0676_implement_magic_dictionary.py) |
| 677 | [Map Sum Pairs](https://leetcode.com/problems/map-sum-pairs/) | Medium | Prefix Aggregation | 前缀累计值、覆盖已有键 | [.py](medium/p0677_map_sum_pairs.py) |
| 720 | [Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/) | Medium | Character Trie | 词终止标记、各级前缀 | [.py](medium/p0720_longest_word_in_dictionary.py) |
| 421 | [Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) | Medium | Bitwise Trie | 固定位宽、异或位优先级 | [.py](medium/p0421_maximum_xor_of_two_numbers_in_an_array.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 1032 | [Stream of Characters](https://leetcode.com/problems/stream-of-characters/) | Hard | Prefix and Suffix | 字符流、Trie 的后缀匹配状态 | [.py](hard/p1032_stream_of_characters.py) |
| 745 | [Prefix and Suffix Search](https://leetcode.com/problems/prefix-and-suffix-search/) | Hard | Prefix and Suffix | 前后缀索引、最大匹配下标 | [.py](hard/p0745_prefix_and_suffix_search.py) |
| 1803 | [Count Pairs With XOR in a Range](https://leetcode.com/problems/count-pairs-with-xor-in-a-range/) | Hard | Bitwise Trie | 位前缀、异或阈值与子树计数 | [.py](hard/p1803_count_pairs_with_xor_in_a_range.py) |
| 2416 | [Sum of Prefix Scores of Strings](https://leetcode.com/problems/sum-of-prefix-scores-of-strings/) | Hard | Prefix Aggregation | 每个前缀的出现次数 | [.py](hard/p2416_sum_of_prefix_scores_of_strings.py) |
