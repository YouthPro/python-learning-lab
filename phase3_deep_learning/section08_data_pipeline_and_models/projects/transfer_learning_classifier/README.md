# transfer_learning_classifier

可独立运行的参考项目，安装仓库 `.[dev,deep-learning]` 后从仓库根目录运行。

## 任务拆分与结构
1. 检查输入/标签与数据划分。
2. 实现并验证数据和模型模块。
3. 调用原生训练循环（不导入练习TODO）。
4. 保存产物，检查结果和边界。

`src/` 分离数据、模型与命令；`tests/` 为CPU离线测试；`scripts/` 存放相关生成入口。共享工具位于 `phase3_deep_learning/common/`。

## 模型、策略与下载边界
ResNet18是主要模型。A只训练fc，B训练layer4+fc，C全部fine-tuning；optimizer在每个策略重新创建。冻结BN的running stats不被训练循环改变。
```bash
# 离线工程验证，随机权重不代表迁移收益
python -m phase3_deep_learning.section08_data_pipeline_and_models.projects.transfer_learning_classifier --dataset synthetic --samples 24 --image-size 32 --epochs 1 --output outputs/phase3/transfer_smoke
# 真实预训练 + 显式CIFAR10下载；也支持fashion_mnist和folder
python -m phase3_deep_learning.section08_data_pipeline_and_models.projects.transfer_learning_classifier --dataset cifar10 --download-data --pretrained --epochs 2 --output outputs/phase3/transfer_real
# 自定义图片目录；--pretrained 单独授权权重下载
python -m phase3_deep_learning.section08_data_pipeline_and_models.projects.transfer_learning_classifier --dataset folder --root outputs/phase3/demo_images --epochs 1 --output outputs/phase3/transfer_folder
python -m phase3_deep_learning.section08_data_pipeline_and_models.projects.transfer_learning_classifier --checkpoint outputs/phase3/transfer_smoke/B/best.pt --input outputs/phase3/demo_images/cat/generated_000.png
```
预训练时固定224 RGB并使用ImageNet mean/std；FashionMNIST经RGB转换。--download-data与--pretrained分别授权数据与权重下载；导入、测试和推理均不下载。推理先构建weights=None的结构再载入完整state_dict。
comparison.csv/json记录val_accuracy、耗时、训练/总参数量。A头部lr=.001，B/C微调lr=.0001，这些是策略配置差异，不把比较说成只改一个变量。验证集用于策略观察，正式结论另留独立test。自动测试用真实随机ResNet检查shape，再用小型stage模型测试完整训练循环，避免GPU与在线权重。
`training_seconds` 统计完整 fit 调用，包含验证、Checkpoint 写入和曲线生成，不含数据加载准备与权重下载；它是端到端训练耗时，不是纯 GPU 算子计时。
验收：A<B<C可训练参数量；A期间backbone参数和BN不动；best.pt可重载对灰度/彩色图片推理，概率和为1。

## 测试
```bash
python -m pytest phase3_deep_learning/section08_data_pipeline_and_models/projects/transfer_learning_classifier/tests
```

训练ResNet在32px输入的最后一组若只有1张图片，BatchNorm没有足够的方差样本；实现仅省略这一张尾样本，验证不会drop。预训练224的eval采用Resize256+CenterCrop224及ImageNet Normalize。
