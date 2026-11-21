# mlp_classifier

可运行参考项目；不读取 exercises 中的 TODO。先安装仓库 `.[dev,deep-learning]`，所有命令在仓库根目录运行。

## 任务拆分
1. 检查数据与shape。
2. 固定种子，划分 Train/Validation/Test。
3. 构建模型、DataLoader和优化器。
4. 训练并按验证集保存最优模型。
5. 重载模型，在test评估与绘图。

## 结构
`src/` 分离数据/模型/训练；共享的项目辅助模块位于 `phase3_deep_learning/common/`（不是练习答案）；`tests/` 只用本地数据。

## 运行与验收
默认 NumPy 生成6000条圆环分类样本，无需外部数据。可比较隐藏层、激活、SGD/Adam和学习率；每个实验使用不同输出目录。Test 只在验证选择最优模型之后评估。数据默认满足>=5000条，--samples 小值仅用于 smoke。

```bash
python -m phase3_deep_learning.section07_pytorch_fundamentals.projects.mlp_classifier --epochs 5 --output outputs/phase3/mlp_demo
python -m phase3_deep_learning.section07_pytorch_fundamentals.projects.mlp_classifier --epochs 5 --hidden 64 32 --activation tanh --optimizer sgd --learning-rate 0.03 --output outputs/phase3/mlp_sgd
```
验收：loss 下降、样本划分互斥、best.pt可加载预测、learning_curves.png与decision_boundary.png有效；比较过拟合时检查训练/验证差异，不依据test选参。

## 测试
```bash
python -m pytest phase3_deep_learning/section07_pytorch_fundamentals/projects/mlp_classifier/tests
```
输出目录中的可再生实验产物允许重建；不要把已有重要实验输出目录用于新比较。训练/验证CSV和JSONL使用样本加权统计。
