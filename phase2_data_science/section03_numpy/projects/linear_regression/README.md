# Linear Regression From Scratch

## 项目目标与需求

只用 NumPy 完成初始化、前向、MSE、梯度、参数更新和预测；单变量与多变量、Batch 与 Mini-batch Gradient Descent。

## 输入数据

regression.npz 含 X:(N,D)、y:(N,)；API 也支持 X:(N,) 的单变量输入。所有随机性来自局部 default_rng(random_state)。

## 文件结构

src/linear_regression.py 数学/训练；src/visualization.py 绘图；main.py CLI。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase2_data_science.section03_numpy.projects.linear_regression.main --output datasets/processed/numpy_regression
python -m phase2_data_science.section03_numpy.projects.linear_regression.main --batch-size 32 --output datasets/processed/numpy_regression_minibatch
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

parameters.npz、loss.csv、predictions.csv、training.png。loss_history_[0] 为初始损失，后续每项对应一个 epoch。

## 验收标准

有限差分验证梯度；无噪声数据恢复权重与偏置；两种训练方式收敛；保存实际值/预测值及 Loss 曲线。训练代码不使用 sklearn 或 PyTorch。

```bash
python -m pytest phase2_data_science/section03_numpy/projects/linear_regression/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
