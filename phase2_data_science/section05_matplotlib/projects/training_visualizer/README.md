# Training Visualizer

## 项目目标与需求

可视化训练/验证 Loss、Accuracy、学习率，自动标记候选过拟合区间，并比较多次实验。

## 输入数据

CSV 列严格为 epoch,train_loss,val_loss,train_acc,val_acc,learning_rate；数据生成脚本提供两次实验。

## 文件结构

src/training_visualizer.py 提供 load_log、detect_overfitting、visualize 和 main。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase2_data_science.section05_matplotlib.projects.training_visualizer.src.training_visualizer datasets/generated/training_log.csv datasets/generated/training_log_b.csv --patience 3
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

datasets/processed/training_visualizer/ 下 training_comparison.png、overfitting.json、report.md。

## 验收标准

五种曲线完整、实验图例明确；连续 patience 次训练 loss 下降且验证 loss 上升标为候选区间；支持空日志；规则只作诊断提示。

```bash
python -m pytest phase2_data_science/section05_matplotlib/projects/training_visualizer/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
