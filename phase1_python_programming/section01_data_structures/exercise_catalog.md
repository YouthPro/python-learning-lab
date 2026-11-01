# Section 01 练习题目录

约定优先于习惯性题解：按这里的排序、返回类型、缺失值和边界行为实现。

## 01. Word Frequency Counter

- 难度：Easy
- 知识点：dict, Counter, re
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def word_frequency(text: str) -> dict[str, int]
```

提取连续英文字母为单词，统一小写，返回词频字典。

输入输出示例："Hi hi!" → {"hi": 2}；"A,b" → {"a": 1, "b": 1}

边界条件：空文本返回 {}；数字和标点是分隔符。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 02. First Unique Character

- 难度：Easy
- 知识点：dict, str
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def first_unique_char(s: str) -> int
```

返回首个只出现一次的字符的索引，大小写敏感；不存在返回 -1。

输入输出示例："leetcode" → 0；"aabb" → -1

边界条件：空字符串返回 -1；包含空白字符。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 03. Remove Duplicates

- 难度：Easy
- 知识点：set, list
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def deduplicate(items: list) -> list
```

保留可哈希元素首次出现的顺序，返回新列表。

输入输出示例：[2,1,2] → [2,1]；[] → []

边界条件：不修改输入；支持混合可哈希对象。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 04. Two Sum

- 难度：Easy
- 知识点：hash map
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def two_sum(nums: list[int], target: int) -> list[int]
```

按 j 从左到右扫描，返回最先找到的一对索引 [i,j]，i 为补数最早出现的位置。无解返回 []。

输入输出示例：[2,7,11],9 → [0,1]；[3,3],6 → [0,1]

边界条件：不能复用同一元素；支持负数与重复数字。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 05. Group Anagrams

- 难度：Medium
- 知识点：dict, sorted
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def group_anagrams(words: list[str]) -> list[list[str]]
```

将字母异位词分组；分组按首个成员出现顺序排列，组内保持输入顺序，大小写敏感。

输入输出示例：["ab","ba","c"] → [["ab","ba"],["c"]]；[] → []

边界条件：空串可以分组；保留重复项。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 06. Top K Frequent Elements

- 难度：Medium
- 知识点：Counter, heapq
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def top_k_frequent(nums: list[int], k: int) -> list[int]
```

返回最多 k 个频次最高的数字；频次相同按数字升序。k≤0 返回 []。

输入输出示例：[2,1,2,1,3],2 → [1,2]；[9],5 → [9]

边界条件：空输入返回 []；k 可大于不同数字数量。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 07. Merge Intervals

- 难度：Medium
- 知识点：sorting, list
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]
```

合并相交或端点接触的闭区间，按起点升序返回；不修改输入。输入保证 start≤end。

输入输出示例：[[1,3],[2,4]] → [[1,4]]；[[1,2],[2,3]] → [[1,3]]

边界条件：空输入返回 []；处理嵌套区间。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 08. Longest Unique Substring

- 难度：Medium
- 知识点：sliding window
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def longest_unique_substring(s: str) -> int
```

返回不含重复字符的最长连续子串的长度。

输入输出示例："abcabcbb" → 3；"bb" → 1

边界条件：空串为 0；支持 Unicode。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 09. Valid Parentheses

- 难度：Easy
- 知识点：stack
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def is_valid_parentheses(s: str) -> bool
```

判断 ()[]{} 是否正确嵌套。遇到其他字符返回 False。

输入输出示例："([])" → True；"([)]" → False

边界条件：空字符串为 True；单个括号无效。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 10. Flatten Nested List

- 难度：Medium
- 知识点：recursion, list
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def flatten_list(items: list) -> list
```

递归展开嵌套 list；其他对象保留为原子元素。返回新列表。

输入输出示例：[1,[2,[3]]] → [1,2,3]；[[],[4]] → [4]

边界条件：空列表返回 []；元组、字符串不展开；输入无循环引用。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 11. Rotate Matrix

- 难度：Medium
- 知识点：2D list
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def rotate_matrix(matrix: list[list[int]]) -> list[list[int]]
```

返回方阵顺时针旋转 90° 的新矩阵；非方阵抛 ValueError。

输入输出示例：[[1,2],[3,4]] → [[3,1],[4,2]]；[[5]] → [[5]]

边界条件：空列表为 []；不要原地修改。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 12. Matrix Transpose

- 难度：Easy
- 知识点：zip, list
- 文件：[exercises/basic_structures.py](exercises/basic_structures.py)

```python
def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]
```

返回矩形矩阵转置的新列表；不等长行抛 ValueError。

输入输出示例：[[1,2,3],[4,5,6]] → [[1,4],[2,5],[3,6]]；[[]] → []

边界条件：[] 与零列矩阵返回 []。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 13. Moving Average

- 难度：Medium
- 知识点：deque, iterator, generator
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def moving_average(stream: Iterable[float], k: int) -> Iterator
```

产生最近最多 k 个元素的均值（含开始时不满窗口的均值）。

输入输出示例：[1,3,5],2 → [1,2,4]；[],2 → []

边界条件：窗口参数≤0 抛 ValueError；惰性读取，不可一次性 list(iterable)。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 14. Chunked Iterator

- 难度：Medium
- 知识点：deque, iterator, generator
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def chunked(iterable: Iterable, size: int) -> Iterator
```

按 size 产生 list；最后不足 size 的批次保留。

输入输出示例：range(5),2 → [[0,1],[2,3],[4]]；[],2 → []

边界条件：窗口参数≤0 抛 ValueError；惰性读取，不可一次性 list(iterable)。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 15. Sliding Window Generator

- 难度：Medium
- 知识点：deque, iterator, generator
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def sliding_window(iterable: Iterable, k: int) -> Iterator
```

只产生长度恰好 k 的连续 tuple 窗口。

输入输出示例：[1,2,3],2 → [(1,2),(2,3)]；[1],2 → []

边界条件：窗口参数≤0 抛 ValueError；惰性读取，不可一次性 list(iterable)。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 16. Merge Sorted Iterables

- 难度：Medium
- 知识点：heapq, iterator
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def merge_sorted(a: Iterable, b: Iterable) -> Iterator
```

惰性合并两个已升序的可迭代对象，保留重复元素。

输入输出示例：[1,3],[2] → [1,2,3]；[],[] → []

边界条件：允许任一输入为空，不可先消费所有输入。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 17. Binary Insert

- 难度：Easy
- 知识点：bisect
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def binary_insert(nums: list[int], value: int) -> list[int]
```

将 value 插入升序 nums 的合适位置，返回新列表；不修改 nums。

输入输出示例：[1,3],2 → [1,2,3]；[],1 → [1]

边界条件：保留重复值；输入保证已排序。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 18. Log Parser

- 难度：Medium
- 知识点：re, str
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def parse_log_line(line: str) -> dict | None
```

解析 YYYY-MM-DD HH:MM:SS LEVEL message；LEVEL 仅 INFO/WARNING/ERROR/DEBUG。返回 timestamp、level、message 字段；格式不符返回 None，不校验实际日历。

输入输出示例："2025-01-01 12:00:00 INFO ok" → {timestamp:...,level:INFO,message:ok}；"bad" → None

边界条件：空串无效；message 可包含空格但非空。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 19. Email Extractor

- 难度：Easy
- 知识点：re
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def extract_emails(text: str) -> list[str]
```

提取 ASCII 简化邮箱：local 使用字母数字及 ._%+-，域名使用字母数字与 .-，顶级域至少两个字母；保留首次出现顺序并去重。无需实现 RFC 全规范。

输入输出示例："a@b.com a@b.com" → ["a@b.com"]；"none" → []

边界条件：空输入为 []；原样保留大小写。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 20. LRU Cache

- 难度：Medium
- 知识点：OrderedDict, OOP
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
class LRUCache:
    def __init__(self, capacity: int) -> None: ...
    def get(self, key): ...
    def put(self, key, value) -> None: ...
    def __len__(self) -> int: ...
```

实现类：get(key) 未命中返回 -1，命中提升为最新；put(key,value) 写入或更新，超过容量淘汰最旧项；支持 len(cache)。

输入输出示例：capacity=1; put(a,1); get(a) → 1；再 put(b,2); get(a) → -1

边界条件：capacity≤0 抛 ValueError；更新已有键不增加长度。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 21. Memoized Fibonacci

- 难度：Medium
- 知识点：functools.cache
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def memoized_fibonacci(n: int) -> int
```

返回 F(0)=0、F(1)=1 的第 n 项；使用 functools.cache 或 lru_cache。

输入输出示例：0 → 0；10 → 55

边界条件：负数抛 ValueError。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 22. Cartesian Product

- 难度：Easy
- 知识点：itertools.product
- 文件：[exercises/advanced_structures.py](exercises/advanced_structures.py)

```python
def cartesian_pairs(a: Iterable, b: Iterable) -> list[tuple]
```

返回按 a 外层、b 内层顺序的笛卡尔积。

输入输出示例：[1,2],["a"] → [(1,"a"),(2,"a")]；[],[1] → []

边界条件：支持一次性迭代器；允许缓存有限输入。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 23. Consecutive Grouping

- 难度：Medium
- 知识点：itertools.groupby
- 文件：[exercises/iterators_generators.py](exercises/iterators_generators.py)

```python
def group_consecutive(items: Iterable) -> list[tuple]
```

将相邻相等元素压缩为 (value,count)，不合并不相邻的同值元素。

输入输出示例：[1,1,2,1] → [(1,2),(2,1),(1,1)]；[] → []

边界条件：接受一次性迭代器。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 24. Compose Functions

- 难度：Medium
- 知识点：closures, functional
- 文件：[exercises/iterators_generators.py](exercises/iterators_generators.py)

```python
def compose(*functions: Callable) -> Callable
```

从右到左组合一元函数；无函数时返回恒等函数。

输入输出示例：compose(str,abs)(-2) → "2"；compose()(3) → 3

边界条件：保留函数异常。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 25. Safe Map

- 难度：Medium
- 知识点：exceptions, map
- 文件：[exercises/iterators_generators.py](exercises/iterators_generators.py)

```python
def safe_map(func: Callable, iterable: Iterable) -> list
```

对每个元素应用 func，遇到 Exception 时在对应位置返回 None，继续处理；不捕获 BaseException。

输入输出示例：int,["1","x"] → [1,None]；int,[] → []

边界条件：保持长度和顺序。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 26. Timer Decorator

- 难度：Medium
- 知识点：decorator, wraps, perf_counter
- 文件：[exercises/iterators_generators.py](exercises/iterators_generators.py)

```python
def timer(func: Callable) -> Callable
```

包装函数，返回 (原返回值,耗时秒数)，用 perf_counter 计时，保留 __name__；异常原样传播。

输入输出示例：timer(abs)(-2) → (2,非负秒数)；timer(len)([]) → (0,非负秒数)

边界条件：支持位置和关键字参数；不输出 stdout。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 27. Retry Decorator

- 难度：Medium
- 知识点：decorator, closure, wraps
- 文件：[exercises/iterators_generators.py](exercises/iterators_generators.py)

```python
def retry(max_attempts: int) -> Callable
```

遇到 Exception 重试，最多执行 max_attempts 次；成功立即返回，失败重新抛最后一次异常。保留元数据。

输入输出示例：retry(2) 包装首次失败函数 → 第二次成功；retry(1) → 不重试

边界条件：max_attempts≤0 在创建装饰器时抛 ValueError；不捕获 BaseException。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 28. Batch File Generator

- 难度：Medium
- 知识点：generator, files
- 文件：[exercises/iterators_generators.py](exercises/iterators_generators.py)

```python
def iter_file_batches(paths: Iterable[Path], size: int) -> Iterator[list[str]]
```

按 paths 顺序逐行读取 UTF-8 文件，移除换行符，每 size 行产生一个 list；批次可跨文件。

输入输出示例：两个文件各一行，size=2 → [["a","b"]]；空 paths → []

边界条件：size≤0 抛 ValueError；尾批保留；文件异常传播；不可整体读文件。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 29. Lazy Line Reader

- 难度：Easy
- 知识点：yield, context manager
- 文件：[exercises/iterators_generators.py](exercises/iterators_generators.py)

```python
def read_lines(path: str | Path) -> Iterator[str]
```

逐行读取 UTF-8 文本，去掉末尾 CR/LF，其余空白保留。

输入输出示例：文件 "a\nb\n" → ["a","b"]；空文件 → []

边界条件：使用 with 关闭文件；不存在路径抛 FileNotFoundError。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 30. Custom Sort

- 难度：Easy
- 知识点：sorted, key
- 文件：[exercises/iterators_generators.py](exercises/iterators_generators.py)

```python
def custom_sort(items: Iterable, key_func: Callable) -> list
```

按 key_func 升序稳定排序，返回新列表。

输入输出示例：["aaa","b"],len → ["b","aaa"]；[],len → []

边界条件：相同 key 保持输入顺序。

提示：先运行对应测试，理解返回结构，再查官方文档。
