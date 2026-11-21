# fashion_mnist_classifier

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
项目使用 torchvision.datasets.FashionMNIST 和 ToTensor/Normalize，MLP从[ B,1,28,28 ]输出[ B,10 ] logits。支持 CPU / CUDA（--device auto 或 cuda）；CPU默认，不写死加速设备。

```bash
# 离线：合成图片，只检查训练工程，不代表真实 FashionMNIST 指标
python -m phase3_deep_learning.section07_pytorch_fundamentals.projects.fashion_mnist_classifier --synthetic --epochs 2 --output outputs/phase3/fashion_smoke
# 显式下载（只在用户执行这一命令时联网）
python -m phase3_deep_learning.section07_pytorch_fundamentals.projects.fashion_mnist_classifier --download --epochs 5 --output outputs/phase3/fashion_real
# 数据已缓存后不需要 --download；--hidden 可比较不同 MLP
```
验收：训练/验证 loss 与accuracy、confusion_matrix.png/json、errors.png、best.pt/latest.pt与predictions.pt均输出；重载最优权重后在独立test计算指标。错误图为展示逐图缩放，不作为模型输入的 Normalize。

## 测试
```bash
python -m pytest phase3_deep_learning/section07_pytorch_fundamentals/projects/fashion_mnist_classifier/tests
```
输出目录中的可再生实验产物允许重建；不要把已有重要实验输出目录用于新比较。训练/验证CSV和JSONL使用样本加权统计。
