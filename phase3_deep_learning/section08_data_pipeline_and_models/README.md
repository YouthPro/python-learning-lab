# Section 08 — Data Pipeline & Model Architecture

## 学习目标与知识
Advanced：掌握自定义 Dataset、DataLoader 与 collate；计算卷积特征图；构建 CNN 与残差连接；基于 torchvision ResNet18 冻结/微调。
Dataset 定义一个样本，DataLoader 负责批处理。num_workers 是进程数，不是batch大小；pin_memory 对 CUDA 传输可能有益，CPU测试禁用。训练打乱、验证有序；验证禁止随机增强。卷积尺寸考虑 stride/padding/dilation；AdaptivePool 避免把 Linear 写死为28x28。预训练权重需要对应RGB尺寸和Normalize，不能只替换fc。

## 推荐顺序与每题目标
先完成01—06并制作数据目录，再做07—10与CNN项目，最后11—15及迁移学习。详见 [题目目录](exercise_catalog.md)，每题均标注 Input/Output Shape、Expected dtype、梯度/计算图和Hint。

| ID | 题目 / 函数 | 学习目标 |
|---|---|---|
| 01 | Custom Dataset / `CustomDataset` | Check labels remain paired after transform. |
| 02 | Dataset Split / `split_indices` | Use a local generator and test that seed changes ordering. |
| 03 | Class Weights / `compute_class_weights` | Count missing classes without dividing by zero. |
| 04 | Padding Collate / `pad_collate` | Separate sequence lengths from padding value. |
| 05 | Image Manifest / `build_image_manifest` | File suffix is not proof of image validity; projects check corruption separately. |
| 06 | DataLoader Factory / `build_dataloader` | shuffle training only; understand worker subprocesses vs batches. |
| 07 | Conv Output Size / `conv2d_output_size` | Derive effective kernel size with dilation. |
| 08 | Build CNN / `build_cnn` | Avoid a Linear input size tied to 28x28. |
| 09 | Residual Block / `build_residual_block` | Use out-of-place addition; test F=0 and negative x. |
| 10 | Top K Accuracy / `topk_accuracy` | Top-k along class axis, not batch axis. |
| 11 | Freeze Backbone / `freeze_backbone` | Frozen parameters and frozen BatchNorm running stats are distinct. |
| 12 | Unfreeze Last Blocks / `unfreeze_last_n_blocks` | n=0 must not accidentally select all via [-0:]. |
| 13 | Replace Classifier / `replace_classifier` | Do not hard-code feature width; no network request. |
| 14 | Build Image Transforms / `build_transforms` | Train/val must not share random augmentation; ImageNet weights expect matching normalization. |
| 15 | Predict Batch / `predict_batch` | eval alone does not disable gradients. |

## 项目与完成标准
- [Image Dataset Pipeline](projects/image_dataset_pipeline/README.md)：自定义Dataset、损坏检查、确定性split清单、增强与类不平衡统计。
- [CNN Classifier](projects/cnn_image_classifier/README.md)：FashionMNIST真实CNN，比较MLP/深度/batch/LR/dropout并生成实际报告。
- [Transfer Learning](projects/transfer_learning_classifier/README.md)：ResNet18 A/B/C冻结策略、参数数量/时间/准确率和单图片推理。
- 严格练习通过；能独立推算特征图并解释训练策略。可选文本分类不纳入核心验收，不要求Transformer。

## 测试
```bash
python -m pytest phase3_deep_learning/section08_data_pipeline_and_models
python -m pytest phase3_deep_learning/section08_data_pipeline_and_models -m exercise
python -m pytest phase3_deep_learning/section08_data_pipeline_and_models -m exercise --strict-exercises
```
项目测试使用临时生成图片、随机初始化ResNet或小型stage模型，联网会报错，不需要GPU。

## 常见错误与 Debug
- 尺寸不匹配：从[N,C,H,W]逐层写出卷积/池化shape，不要靠随意reshape通过。
- 图片通道不一致：PIL先转RGB，再做Normalize；灰度FashionMNIST迁移到ResNet须转3通道。
- 全部被冻结：替换head后再确认requires_grad列表，改变冻结策略后重建optimizer。
- BN漂移：冻结参数并不冻结running_mean；参考训练循环对冻结BN设eval。
- 验证随机变动：确认使用独立eval transform，split索引固定且没有泄漏。
- worker问题：先num_workers=0，避免lambda在spawn中不可序列化；脚本使用main保护。

## 官方资料
- [Dataset与DataLoader](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)
- [Torchvision](https://pytorch.org/vision/stable/index.html)
- [Transfer Learning](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [ResNet18权重与预处理](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html)
