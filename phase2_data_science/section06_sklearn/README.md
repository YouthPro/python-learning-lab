# Section 06: Scikit-learn & Machine Learning Workflow

## 学习目标

建立无数据泄漏、可比较、可保存和复用的机器学习流程。 学习者已掌握基础语法；本节不重复讲变量、循环与条件判断。

## 知识点

train_test_split、SimpleImputer/StandardScaler/Pipeline、回归和分类指标、KFold/StratifiedKFold、GridSearchCV、joblib。

## 推荐学习顺序

先读 [题目目录](exercise_catalog.md)，按 preprocessing → model_evaluation → model_selection 的顺序完成练习；每题先理解边界契约，再写代码并运行对应测试。最后完成/阅读项目并在小数据上独立解释输出。

```bash
python -m pytest phase2_data_science/section06_sklearn/tests -q
python -m pytest phase2_data_science/section06_sklearn -q
python -m pytest phase2_data_science/section06_sklearn/tests --strict-exercises -q
```

未修改的 TODO 默认显示 xfail；实现后断言会正常执行，错误实现会失败。严格模式中所有 TODO 都失败。默认通过不代表练习已完成。浮点结果使用 allclose 或 approx，随机样例固定种子。

## 练习与进度

- [ ] Exercise 01: [Train Test Split](exercise_catalog.md#01-train-test-split) — `split_dataset`
- [ ] Exercise 02: [Feature Scaling](exercise_catalog.md#02-feature-scaling) — `scale_features`
- [ ] Exercise 03: [Missing Value Pipeline](exercise_catalog.md#03-missing-value-pipeline) — `build_preprocessing_pipeline`
- [ ] Exercise 04: [Regression Metrics](exercise_catalog.md#04-regression-metrics) — `regression_metrics`
- [ ] Exercise 05: [Classification Metrics](exercise_catalog.md#05-classification-metrics) — `classification_metrics`
- [ ] Exercise 06: [Confusion Matrix](exercise_catalog.md#06-confusion-matrix) — `plot_confusion_matrix`
- [ ] Exercise 07: [Cross Validation](exercise_catalog.md#07-cross-validation) — `evaluate_cv`
- [ ] Exercise 08: [Hyperparameter Search](exercise_catalog.md#08-hyperparameter-search) — `search_best_params`

## 项目与进度

- [ ] [Machine Learning Workflow](projects/machine_learning_workflow/README.md)

## 完成标准

全部 8 道契约测试在严格模式通过；能解释数据结构选择、时间/空间开销和边界处理；项目满足各自 README 中的验收标准并产出报告。NumPy 练习优先使用向量化，避免逐元素 Python 循环；图形练习返回 Figure/Axes，不调用 show。

## 官方参考资料与练习平台

- [Scikit-learn 官方入门](https://scikit-learn.org/stable/getting_started.html)
