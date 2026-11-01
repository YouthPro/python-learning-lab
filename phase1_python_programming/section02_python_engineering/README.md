# Section 02: Python Engineering & File Processing

## 学习目标

从单函数过渡到可测试的命令行项目；保持 Phase 1 主要依赖标准库。 学习者已掌握基础语法；本节不重复讲变量、循环与条件判断。

## 知识点

pathlib/csv/json/hashlib、try/except/异常链、logging、dataclass、Type Hint、组合与特殊方法、pytest。

## 推荐学习顺序

先读 [题目目录](exercise_catalog.md)，按 file_operations → error_handling → oop_and_testing 的顺序完成练习；每题先理解边界契约，再写代码并运行对应测试。最后完成/阅读项目并在小数据上独立解释输出。

```bash
python -m pytest phase1_python_programming/section02_python_engineering/tests -q
python -m pytest phase1_python_programming/section02_python_engineering -q
python -m pytest phase1_python_programming/section02_python_engineering/tests --strict-exercises -q
```

未修改的 TODO 默认显示 xfail；实现后断言会正常执行，错误实现会失败。严格模式中所有 TODO 都失败。默认通过不代表练习已完成。浮点结果使用 allclose 或 approx，随机样例固定种子。

## 练习与进度

- [ ] Exercise 01: [List Files Recursively](exercise_catalog.md#01-list-files-recursively) — `list_files`
- [ ] Exercise 02: [CSV Reader](exercise_catalog.md#02-csv-reader) — `read_csv`
- [ ] Exercise 03: [JSON Normalizer](exercise_catalog.md#03-json-normalizer) — `normalize_json`
- [ ] Exercise 04: [File Hash Calculator](exercise_catalog.md#04-file-hash-calculator) — `calculate_file_hash`
- [ ] Exercise 05: [Duplicate File Finder](exercise_catalog.md#05-duplicate-file-finder) — `find_duplicates`
- [ ] Exercise 06: [Safe Batch Rename](exercise_catalog.md#06-safe-batch-rename) — `batch_rename`
- [ ] Exercise 07: [Logged JSON Loader](exercise_catalog.md#07-logged-json-loader) — `load_json_safely`
- [ ] Exercise 08: [Dataset Record](exercise_catalog.md#08-dataset-record) — `DatasetRecord`
- [ ] Exercise 09: [Dataset Collection](exercise_catalog.md#09-dataset-collection) — `DatasetCollection`

## 项目与进度

- [ ] [File Toolkit](projects/file_toolkit/README.md)
- [ ] [Dataset Inspector](projects/dataset_inspector/README.md)
- [ ] [Dataset Cleaning Pipeline](projects/dataset_cleaning_pipeline/README.md)

## 完成标准

全部 9 道契约测试在严格模式通过；能解释数据结构选择、时间/空间开销和边界处理；项目满足各自 README 中的验收标准并产出报告。NumPy 练习优先使用向量化，避免逐元素 Python 循环；图形练习返回 Figure/Axes，不调用 show。

## 官方参考资料与练习平台

- [Python 标准库](https://docs.python.org/3/library/)
- [pytest 入门](https://docs.pytest.org/en/stable/getting-started.html)
