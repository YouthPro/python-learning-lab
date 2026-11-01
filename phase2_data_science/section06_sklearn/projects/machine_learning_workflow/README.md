# Machine Learning Workflow

## 项目目标与需求

完整实现回归与二分类：数据读取、训练集 EDA、缺失处理、标准化、三模型比较、CV、GridSearchCV、留出评估和 joblib 保存/加载预测。

## 输入数据

模拟房价特征 area,bedrooms,bathrooms,house_age,distance_to_city,location_score，目标 price；分类数据由 make_classification 固定种子生成，10 个特征，目标 target。

## 文件结构

configs/config.yaml；src/data_loader.py、preprocessing.py、models.py、evaluation.py、visualization.py、pipeline.py；main.py；models/；reports/；tests/。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase2_data_science.section06_sklearn.projects.machine_learning_workflow.main --task all
python -m phase2_data_science.section06_sklearn.projects.machine_learning_workflow.main --predict-model phase2_data_science/section06_sklearn/projects/machine_learning_workflow/models/regression.joblib --input datasets/generated/housing.csv --predictions datasets/processed/house_predictions.csv
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

models/ 中保存两个完整 Pipeline。reports/ 中提供 MAE/MSE/RMSE/R2 或 Accuracy/Precision/Recall/F1/混淆矩阵、三个模型的 CV 比较、GridSearchCV 候选、测试集预测与 EDA 图。

## 验收标准

划分后在每折训练集内 fit imputer/scaler；分类分层划分；按训练 CV 选择最终模型，测试集仅评估一次。回归比较 LinearRegression/RandomForest/GradientBoosting；分类比较 LogisticRegression/RandomForest/SVM。所有随机过程可配置 random_state，持久化前后预测一致。

```bash
python -m pytest phase2_data_science/section06_sklearn/projects/machine_learning_workflow/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
