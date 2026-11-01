# Section 04: Pandas & Data Analysis

## 学习目标

独立处理结构化数据、发现质量问题并完成可复现分析。 学习者已掌握基础语法；本节不重复讲变量、循环与条件判断。

## 知识点

DataFrame、索引、缺失值、可空 dtype、日期、去重、IQR、groupby/transform、merge/pivot/rolling。

## 推荐学习顺序

先读 [题目目录](exercise_catalog.md)，按 dataframe_basics → data_cleaning → groupby_merge 的顺序完成练习；每题先理解边界契约，再写代码并运行对应测试。最后完成/阅读项目并在小数据上独立解释输出。

```bash
python -m pytest phase2_data_science/section04_pandas/tests -q
python -m pytest phase2_data_science/section04_pandas -q
python -m pytest phase2_data_science/section04_pandas/tests --strict-exercises -q
```

未修改的 TODO 默认显示 xfail；实现后断言会正常执行，错误实现会失败。严格模式中所有 TODO 都失败。默认通过不代表练习已完成。浮点结果使用 allclose 或 approx，随机样例固定种子。

## 练习与进度

- [ ] Exercise 01: [Load Dataset](exercise_catalog.md#01-load-dataset) — `load_dataset`
- [ ] Exercise 02: [Select Columns](exercise_catalog.md#02-select-columns) — `select_columns`
- [ ] Exercise 03: [Conditional Filtering](exercise_catalog.md#03-conditional-filtering) — `filter_rows`
- [ ] Exercise 04: [Column Transformation](exercise_catalog.md#04-column-transformation) — `transform_column`
- [ ] Exercise 05: [Date Conversion](exercise_catalog.md#05-date-conversion) — `convert_dates`
- [ ] Exercise 06: [Data Type Conversion](exercise_catalog.md#06-data-type-conversion) — `convert_dtypes`
- [ ] Exercise 07: [Missing Value Analysis](exercise_catalog.md#07-missing-value-analysis) — `missing_summary`
- [ ] Exercise 08: [Missing Value Imputation](exercise_catalog.md#08-missing-value-imputation) — `fill_missing`
- [ ] Exercise 09: [Duplicate Removal](exercise_catalog.md#09-duplicate-removal) — `remove_duplicates`
- [ ] Exercise 10: [Outlier Detection](exercise_catalog.md#10-outlier-detection) — `detect_outliers`
- [ ] Exercise 11: [Group Statistics](exercise_catalog.md#11-group-statistics) — `group_statistics`
- [ ] Exercise 12: [Group Transformation](exercise_catalog.md#12-group-transformation) — `group_transform`
- [ ] Exercise 13: [Merge Tables](exercise_catalog.md#13-merge-tables) — `merge_tables`
- [ ] Exercise 14: [Pivot Data](exercise_catalog.md#14-pivot-data) — `create_pivot`
- [ ] Exercise 15: [Rolling Average](exercise_catalog.md#15-rolling-average) — `rolling_average`

## 项目与进度

- [ ] [E-commerce Data Analysis](projects/ecommerce_analysis/README.md)

## 完成标准

全部 15 道契约测试在严格模式通过；能解释数据结构选择、时间/空间开销和边界处理；项目满足各自 README 中的验收标准并产出报告。NumPy 练习优先使用向量化，避免逐元素 Python 循环；图形练习返回 Figure/Axes，不调用 show。

## 官方参考资料与练习平台

- [Pandas 官方教程](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)
- [LeetCode Pandas 练习（第三方）](https://leetcode.com/studyplan/introduction-to-pandas/)
