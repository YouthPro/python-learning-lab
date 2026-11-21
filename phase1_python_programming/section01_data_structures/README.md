# Section 01: Python Data Structures & Algorithms

## 学习目标

熟练使用内置结构、标准库、函数、迭代器与生成器。 学习者已掌握基础语法；本节不重复讲变量、循环与条件判断。

## 知识点

dict/set/list、Counter/deque/heapq/bisect/re、OrderedDict、cache、itertools、装饰器与文件生成器。

## LeetCode 数据结构专项

专项练习按 12 种数据结构和难度组织，共 141 道题。每题提供可独立导入的 Python3 骨架，并在章节目录中标明训练方向。 [专项练习目录](leetcode-data-structures-python/README.md)

## 推荐学习顺序

先读 [题目目录](exercise_catalog.md)，按 basic_structures → advanced_structures → iterators_generators 的顺序完成练习；每题先理解边界契约，再写代码并运行对应测试。最后完成/阅读项目并在小数据上独立解释输出。

```bash
python -m pytest phase1_python_programming/section01_data_structures/tests -q
python -m pytest phase1_python_programming/section01_data_structures -q
python -m pytest phase1_python_programming/section01_data_structures/tests --strict-exercises -q
```

未修改的 TODO 默认显示 xfail；实现后断言会正常执行，错误实现会失败。严格模式中所有 TODO 都失败。默认通过不代表练习已完成。浮点结果使用 allclose 或 approx，随机样例固定种子。

## Advanced Time Tests / Advanced Memory Tests

30 道题各有一项时间压力测试和一项内存压力测试。提交实现后可生成正确性、时间用量/时间限制、内存用量/内存限制及对应比值：

```bash
python scripts/assess_section01.py --problem two_sum
python scripts/assess_section01.py
```

报告保存为 `datasets/processed/section01_assessment/results.json` 和 `results.md`。只有正确性、时间和内存全部达标才通过；TODO 显示未实现，不伪造性能数据。

压力测试默认不随日常测试运行，使用 `--run-advanced` 启用；时间与内存分开在独立进程中测量。内存指执行期间的 Python 分配峰值，包含返回结果、不包含预先构造的输入，不等于进程 RSS。完整的逐题限制、工作负载、复杂度目标与运行命令见 [性能评估指南](../../docs/section01_performance.md)。

## 练习与进度

- [ ] Exercise 01: [Word Frequency Counter](exercise_catalog.md#01-word-frequency-counter) — `word_frequency`
- [ ] Exercise 02: [First Unique Character](exercise_catalog.md#02-first-unique-character) — `first_unique_char`
- [ ] Exercise 03: [Remove Duplicates](exercise_catalog.md#03-remove-duplicates) — `deduplicate`
- [ ] Exercise 04: [Two Sum](exercise_catalog.md#04-two-sum) — `two_sum`
- [ ] Exercise 05: [Group Anagrams](exercise_catalog.md#05-group-anagrams) — `group_anagrams`
- [ ] Exercise 06: [Top K Frequent Elements](exercise_catalog.md#06-top-k-frequent-elements) — `top_k_frequent`
- [ ] Exercise 07: [Merge Intervals](exercise_catalog.md#07-merge-intervals) — `merge_intervals`
- [ ] Exercise 08: [Longest Unique Substring](exercise_catalog.md#08-longest-unique-substring) — `longest_unique_substring`
- [ ] Exercise 09: [Valid Parentheses](exercise_catalog.md#09-valid-parentheses) — `is_valid_parentheses`
- [ ] Exercise 10: [Flatten Nested List](exercise_catalog.md#10-flatten-nested-list) — `flatten_list`
- [ ] Exercise 11: [Rotate Matrix](exercise_catalog.md#11-rotate-matrix) — `rotate_matrix`
- [ ] Exercise 12: [Matrix Transpose](exercise_catalog.md#12-matrix-transpose) — `transpose_matrix`
- [ ] Exercise 13: [Moving Average](exercise_catalog.md#13-moving-average) — `moving_average`
- [ ] Exercise 14: [Chunked Iterator](exercise_catalog.md#14-chunked-iterator) — `chunked`
- [ ] Exercise 15: [Sliding Window Generator](exercise_catalog.md#15-sliding-window-generator) — `sliding_window`
- [ ] Exercise 16: [Merge Sorted Iterables](exercise_catalog.md#16-merge-sorted-iterables) — `merge_sorted`
- [ ] Exercise 17: [Binary Insert](exercise_catalog.md#17-binary-insert) — `binary_insert`
- [ ] Exercise 18: [Log Parser](exercise_catalog.md#18-log-parser) — `parse_log_line`
- [ ] Exercise 19: [Email Extractor](exercise_catalog.md#19-email-extractor) — `extract_emails`
- [ ] Exercise 20: [LRU Cache](exercise_catalog.md#20-lru-cache) — `LRUCache`
- [ ] Exercise 21: [Memoized Fibonacci](exercise_catalog.md#21-memoized-fibonacci) — `memoized_fibonacci`
- [ ] Exercise 22: [Cartesian Product](exercise_catalog.md#22-cartesian-product) — `cartesian_pairs`
- [ ] Exercise 23: [Consecutive Grouping](exercise_catalog.md#23-consecutive-grouping) — `group_consecutive`
- [ ] Exercise 24: [Compose Functions](exercise_catalog.md#24-compose-functions) — `compose`
- [ ] Exercise 25: [Safe Map](exercise_catalog.md#25-safe-map) — `safe_map`
- [ ] Exercise 26: [Timer Decorator](exercise_catalog.md#26-timer-decorator) — `timer`
- [ ] Exercise 27: [Retry Decorator](exercise_catalog.md#27-retry-decorator) — `retry`
- [ ] Exercise 28: [Batch File Generator](exercise_catalog.md#28-batch-file-generator) — `iter_file_batches`
- [ ] Exercise 29: [Lazy Line Reader](exercise_catalog.md#29-lazy-line-reader) — `read_lines`
- [ ] Exercise 30: [Custom Sort](exercise_catalog.md#30-custom-sort) — `custom_sort`

## 项目与进度

- [ ] [Text Analyzer](projects/text_analyzer/README.md)

## 完成标准

全部 30 道契约测试在严格模式通过；能解释数据结构选择、时间/空间开销和边界处理；项目满足各自 README 中的验收标准并产出报告。NumPy 练习优先使用向量化，避免逐元素 Python 循环；图形练习返回 Figure/Axes，不调用 show。

## 官方参考资料与练习平台

- [Python 标准库](https://docs.python.org/3/library/)
- [Exercism Python 练习（第三方）](https://exercism.org/tracks/python)
- [LeetCode 题库（第三方）](https://leetcode.com/problemset/)
