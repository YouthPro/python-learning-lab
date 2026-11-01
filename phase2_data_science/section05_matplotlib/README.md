# Section 05: Matplotlib & Data Visualization

## 学习目标

使用 Object-Oriented API 绘制统计图并解释分布、相关性和训练曲线。 学习者已掌握基础语法；本节不重复讲变量、循环与条件判断。

## 知识点

Figure/Axes、折线/柱图/直方/散点/箱线、色图、子图、图例、PNG 与资源释放。

## 推荐学习顺序

先读 [题目目录](exercise_catalog.md)，按 basic_plots → advanced_plots 的顺序完成练习；每题先理解边界契约，再写代码并运行对应测试。最后完成/阅读项目并在小数据上独立解释输出。

```bash
python -m pytest phase2_data_science/section05_matplotlib/tests -q
python -m pytest phase2_data_science/section05_matplotlib -q
python -m pytest phase2_data_science/section05_matplotlib/tests --strict-exercises -q
```

未修改的 TODO 默认显示 xfail；实现后断言会正常执行，错误实现会失败。严格模式中所有 TODO 都失败。默认通过不代表练习已完成。浮点结果使用 allclose 或 approx，随机样例固定种子。

## 练习与进度

- [ ] Exercise 01: [Line Plot](exercise_catalog.md#01-line-plot) — `plot_line`
- [ ] Exercise 02: [Bar Chart](exercise_catalog.md#02-bar-chart) — `plot_bar`
- [ ] Exercise 03: [Histogram](exercise_catalog.md#03-histogram) — `plot_hist`
- [ ] Exercise 04: [Scatter Plot](exercise_catalog.md#04-scatter-plot) — `plot_scatter`
- [ ] Exercise 05: [Box Plot](exercise_catalog.md#05-box-plot) — `plot_box`
- [ ] Exercise 06: [Correlation Heatmap](exercise_catalog.md#06-correlation-heatmap) — `plot_correlation`
- [ ] Exercise 07: [Multiple Subplots](exercise_catalog.md#07-multiple-subplots) — `plot_dashboard`
- [ ] Exercise 08: [Save Figure](exercise_catalog.md#08-save-figure) — `save_figure`

## 项目与进度

- [ ] [Exploratory Data Analysis Report](projects/exploratory_data_analysis/README.md)
- [ ] [Training Visualizer](projects/training_visualizer/README.md)

## 完成标准

全部 8 道契约测试在严格模式通过；能解释数据结构选择、时间/空间开销和边界处理；项目满足各自 README 中的验收标准并产出报告。NumPy 练习优先使用向量化，避免逐元素 Python 循环；图形练习返回 Figure/Axes，不调用 show。

## 官方参考资料与练习平台

- [Matplotlib 官方教程](https://matplotlib.org/stable/tutorials/index.html)
