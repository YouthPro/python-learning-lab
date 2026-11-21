# Section 03 · Stack

## 数据结构

栈采用后进先出的访问顺序。Python 的 `list` 尾部可以作为栈顶。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 入栈、出栈、读取栈顶和检查空栈。 |
| 时间复杂度 | 尾部入栈和出栈均摊 `O(1)`，查看栈顶和判断是否为空为 `O(1)`。 |
| 空间复杂度 | 栈占 `O(n)` 空间，其中 `n` 是同时留在栈中的最大元素数。 |
| 常见使用场景 | 括号匹配、撤销和回退、表达式求值、最近更大或更小元素。 |

## 核心知识点

Basic Stack 关注栈顶状态，Monotonic Stack 关注入栈与出栈时的顺序不变量，Expression Evaluation 关注操作数、嵌套层级与求值顺序。

## 题目

本节共 12 题。子方向对应 YAML 中的 `subsection`。

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 20 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Basic Stack | 括号成对匹配、空栈边界 | [.py](easy/p0020_valid_parentheses.py) |
| 682 | [Baseball Game](https://leetcode.com/problems/baseball-game/) | Easy | Basic Stack | 操作记录、回退与栈顶读取 | [.py](easy/p0682_baseball_game.py) |
| 1047 | [Remove All Adjacent Duplicates In String](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/) | Easy | Basic Stack | 相邻字符匹配、消除后的栈顶 | [.py](easy/p1047_remove_all_adjacent_duplicates_in_string.py) |
| 844 | [Backspace String Compare](https://leetcode.com/problems/backspace-string-compare/) | Easy | Basic Stack | 退格语义、编辑后的字符序列 | [.py](easy/p0844_backspace_string_compare.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 150 | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Medium | Expression Evaluation | 逆波兰表示、操作数次序 | [.py](medium/p0150_evaluate_reverse_polish_notation.py) |
| 394 | [Decode String](https://leetcode.com/problems/decode-string/) | Medium | Expression Evaluation | 嵌套表达式、重复次数与字符串片段 | [.py](medium/p0394_decode_string.py) |
| 735 | [Asteroid Collision](https://leetcode.com/problems/asteroid-collision/) | Medium | Basic Stack | 模拟冲突、保留未消解状态 | [.py](medium/p0735_asteroid_collision.py) |
| 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Monotonic Stack | 单调下标栈、等待距离 | [.py](medium/p0739_daily_temperatures.py) |
| 946 | [Validate Stack Sequences](https://leetcode.com/problems/validate-stack-sequences/) | Medium | Basic Stack | 入栈与出栈序列、模拟边界 | [.py](medium/p0946_validate_stack_sequences.py) |
| 402 | [Remove K Digits](https://leetcode.com/problems/remove-k-digits/) | Medium | Monotonic Stack | 单调性、删除预算与前导零 | [.py](medium/p0402_remove_k_digits.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 84 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | Monotonic Stack | 高度顺序、矩形左右边界 | [.py](hard/p0084_largest_rectangle_in_histogram.py) |
| 32 | [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | Hard | Basic Stack | 括号下标、连续有效区间 | [.py](hard/p0032_longest_valid_parentheses.py) |
