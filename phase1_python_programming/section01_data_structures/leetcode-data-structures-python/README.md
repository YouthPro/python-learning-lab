# leetcode-data-structures-python

按 Section、Subsection 和难度组织的 Python 数据结构专项训练，共 12 个 Section、141 道 LeetCode 题。每题有一个独立的 Python3 骨架，方法体统一为 `raise NotImplementedError`。各节 README 列出每题的训练方向。

## 环境

使用 Python 3.11 或更新版本。练习和骨架检查使用标准库。

## 训练目录

| Section | 数据结构 | Easy | Medium | Hard | 合计 |
| --- | --- | --- | --- | --- | --- |
| 01 | [Array](sections/01_array/README.md) | 5 | 5 | 3 | 13 |
| 02 | [Linked List](sections/02_linked_list/README.md) | 8 | 6 | 1 | 15 |
| 03 | [Stack](sections/03_stack/README.md) | 4 | 6 | 2 | 12 |
| 04 | [Queue / Deque](sections/04_queue_deque/README.md) | 4 | 6 | 1 | 11 |
| 05 | [HashMap](sections/05_hash_map/README.md) | 6 | 3 | 1 | 10 |
| 06 | [HashSet](sections/06_hash_set/README.md) | 7 | 3 | 0 | 10 |
| 07 | [Heap / Priority Queue](sections/07_heap/README.md) | 3 | 5 | 2 | 10 |
| 08 | [Binary Tree](sections/08_binary_tree/README.md) | 10 | 3 | 2 | 15 |
| 09 | [Binary Search Tree](sections/09_bst/README.md) | 5 | 7 | 1 | 13 |
| 10 | [Trie](sections/10_trie/README.md) | 0 | 7 | 4 | 11 |
| 11 | [Graph](sections/11_graph/README.md) | 3 | 6 | 1 | 10 |
| 12 | [Union-Find](sections/12_union_find/README.md) | 0 | 10 | 1 | 11 |
|  | **合计** | 55 | 67 | 19 | 141 |

## 开始练习

1. 从 Python Learning Lab 根目录进入本项目。

   ```bash
   cd phase1_python_programming/section01_data_structures/leetcode-data-structures-python
   python --version
   ```

2. 在选定的 Section 中按 **Easy → Medium → Hard** 的顺序练习，从该节第一种有题的难度开始。通过 Section README 查找题目的官方页面和本地骨架。
3. 保留类名、方法名、参数和返回类型。完成练习时替换相应的 `raise NotImplementedError`，并运行题目的公开样例。

## 单一数据结构约束

每题使用题库的 `primary_data_structure`。辅助状态限定为题目的输入和输出、普通变量、指针、索引、递归调用栈和目标数据结构的内部状态。同种数据结构可使用多个实例。Graph 节用图和递归 DFS，可记录简单访问状态。各节的题目表列出具体训练方向。

## 本地测试

在本项目根目录检查骨架语法。

```bash
python -m compileall -q common sections
```

逐个导入题目以及添加本地用例的命令见测试说明。 [本地测试](tests/README.md)

## 提交到 LeetCode

在官方题目页选择 Python3，粘贴练习完成的类和所需的标准库导入，运行用例后提交。链表和树的节点由 LeetCode 提供，提交时移除本地的 `from common.nodes import ...` 导入。会员题 346 的公开同题接口见力扣 LCR 041，主站 Python3 模板待核实。 [力扣 LCR 041](https://leetcode.cn/problems/qIsx9U/)

## 练习进度

题目的默认状态为 `TODO`。在 YAML 按编号修改 `status`，并同步进度表中的对应行。 [YAML 题库](catalog/problems.yaml) · [进度表](CATALOG.md)

| 状态 | 含义 |
| --- | --- |
| `TODO` | 待开始 |
| `IN_PROGRESS` | 实现或验证中 |
| `SOLVED` | 已通过 LeetCode 提交 |
| `REVIEW` | 已完成一轮并待复习 |
