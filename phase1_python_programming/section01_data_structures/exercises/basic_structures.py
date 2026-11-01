from __future__ import annotations


def word_frequency(text: str) -> dict[str, int]:
    """01. Word Frequency Counter
    Difficulty: Easy
    知识点: dict, Counter, re

    提取连续英文字母为单词，统一小写，返回词频字典。

    示例: "Hi hi!" → {"hi": 2}；"A,b" → {"a": 1, "b": 1}
    边界: 空文本返回 {}；数字和标点是分隔符。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def first_unique_char(s: str) -> int:
    """02. First Unique Character
    Difficulty: Easy
    知识点: dict, str

    返回首个只出现一次的字符的索引，大小写敏感；不存在返回 -1。

    示例: "leetcode" → 0；"aabb" → -1
    边界: 空字符串返回 -1；包含空白字符。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def deduplicate(items: list) -> list:
    """03. Remove Duplicates
    Difficulty: Easy
    知识点: set, list

    保留可哈希元素首次出现的顺序，返回新列表。

    示例: [2,1,2] → [2,1]；[] → []
    边界: 不修改输入；支持混合可哈希对象。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def two_sum(nums: list[int], target: int) -> list[int]:
    """04. Two Sum
    Difficulty: Easy
    知识点: hash map

    按 j 从左到右扫描，返回最先找到的一对索引 [i,j]，i 为补数最早出现的位置。无解返回 []。

    示例: [2,7,11],9 → [0,1]；[3,3],6 → [0,1]
    边界: 不能复用同一元素；支持负数与重复数字。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def group_anagrams(words: list[str]) -> list[list[str]]:
    """05. Group Anagrams
    Difficulty: Medium
    知识点: dict, sorted

    将字母异位词分组；分组按首个成员出现顺序排列，组内保持输入顺序，大小写敏感。

    示例: ["ab","ba","c"] → [["ab","ba"],["c"]]；[] → []
    边界: 空串可以分组；保留重复项。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """06. Top K Frequent Elements
    Difficulty: Medium
    知识点: Counter, heapq

    返回最多 k 个频次最高的数字；频次相同按数字升序。k≤0 返回 []。

    示例: [2,1,2,1,3],2 → [1,2]；[9],5 → [9]
    边界: 空输入返回 []；k 可大于不同数字数量。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """07. Merge Intervals
    Difficulty: Medium
    知识点: sorting, list

    合并相交或端点接触的闭区间，按起点升序返回；不修改输入。输入保证 start≤end。

    示例: [[1,3],[2,4]] → [[1,4]]；[[1,2],[2,3]] → [[1,3]]
    边界: 空输入返回 []；处理嵌套区间。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def longest_unique_substring(s: str) -> int:
    """08. Longest Unique Substring
    Difficulty: Medium
    知识点: sliding window

    返回不含重复字符的最长连续子串的长度。

    示例: "abcabcbb" → 3；"bb" → 1
    边界: 空串为 0；支持 Unicode。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def is_valid_parentheses(s: str) -> bool:
    """09. Valid Parentheses
    Difficulty: Easy
    知识点: stack

    判断 ()[]{} 是否正确嵌套。遇到其他字符返回 False。

    示例: "([])" → True；"([)]" → False
    边界: 空字符串为 True；单个括号无效。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def flatten_list(items: list) -> list:
    """10. Flatten Nested List
    Difficulty: Medium
    知识点: recursion, list

    递归展开嵌套 list；其他对象保留为原子元素。返回新列表。

    示例: [1,[2,[3]]] → [1,2,3]；[[],[4]] → [4]
    边界: 空列表返回 []；元组、字符串不展开；输入无循环引用。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def rotate_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """11. Rotate Matrix
    Difficulty: Medium
    知识点: 2D list

    返回方阵顺时针旋转 90° 的新矩阵；非方阵抛 ValueError。

    示例: [[1,2],[3,4]] → [[3,1],[4,2]]；[[5]] → [[5]]
    边界: 空列表为 []；不要原地修改。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """12. Matrix Transpose
    Difficulty: Easy
    知识点: zip, list

    返回矩形矩阵转置的新列表；不等长行抛 ValueError。

    示例: [[1,2,3],[4,5,6]] → [[1,4],[2,5],[3,6]]；[[]] → []
    边界: [] 与零列矩阵返回 []。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
