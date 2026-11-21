# Section 07 — PyTorch Fundamentals

## 学习目标与知识
从 NumPy 的 shape/dtype 迁移到 Tensor、device 和计算图；亲手构造标量损失并追踪链式求导，最后组织 nn.Module 与标准优化循环。难度 Medium → Advanced。

Tensor 默认浮点是 float32，分类标签是 long；CrossEntropyLoss 接收 logits。reshape 可能复制，view 有连续性约束。requires_grad、model.train/eval、no_grad 分别控制不同机制；梯度默认累加，验证不应更新参数或 BatchNorm 状态。

## 推荐顺序
先做 tensor_operations 01—08，再在纸上推导 autograd 09—13，最后实现 neural_network 14—18；随后完成 MLP Classifier，再训练 FashionMNIST。详细 Input/Output Shape、Expected dtype、计算图契约和 Hint 在 [题目目录](exercise_catalog.md)，函数 docstring 同样保留。

## 每题目标

| ID | 题目 / 函数 | 目标 |
|---|---|---|
| 01 | Tensor Factory / `create_tensor` | Compare tensor construction with as_tensor; validate dtype in tests. |
| 02 | Shape Transformation / `transform_tensor` | Think about when view requires contiguous memory. |
| 03 | Add Batch Dimension / `add_batch_dim` | Read the legal range of unsqueeze dimensions. |
| 04 | Last Dimension Normalization / `normalize_last_dim` | Keep reduced axes for broadcasting; explain singleton std. |
| 05 | Masked Row Selection / `select_rows` | Check mask length and dtype; M may be zero. |
| 06 | Pairwise Cosine Similarity / `pairwise_cosine_similarity` | Sketch matrix multiplication axes before coding. |
| 07 | Recursive Device Transfer / `move_to_device` | Use type checks; strings must not be treated as sequences. |
| 08 | NumPy Interoperability / `to_numpy` | Explain why direct numpy fails on requires_grad=True or CUDA. |
| 09 | Scalar Gradient / `compute_scalar_gradient` | On paper: derivative of each power, then add. Avoid wrapping an existing graph accidentally. |
| 10 | Vector Gradient / `compute_vector_gradient` | Each coordinate contributes independently; explain the chain rule through sum. |
| 11 | Gradient Accumulation / `gradient_accumulation_demo` | Track addition into .grad, then explain why clearing it changes the third result. |
| 12 | Detach Tensor / `detach_tensor` | Detach affects this tensor; no_grad affects operations in its context. |
| 13 | Freeze Parameters / `freeze_parameters` | requires_grad and eval control different behavior; explain BatchNorm/dropout. |
| 14 | Build MLP / `build_mlp` | List layer dimensions first; CrossEntropyLoss expects logits. |
| 15 | Count Parameters / `count_parameters` | Buffers are not parameters; specify whether frozen parameters count. |
| 16 | One Training Epoch / `train_one_epoch` | Set train mode, transfer both tensors; last batch may be smaller. |
| 17 | Model Evaluation / `evaluate` | eval does not disable autograd by itself; multiply mean loss by batch size. |
| 18 | Probability Prediction / `predict_proba` | Apply softmax over classes, not batch; detach before moving outputs. |

## 项目要求与完成标准
- [MLP Classifier](projects/mlp_classifier/README.md)：6000 条二维非线性数据、独立划分、训练与验证曲线、最优模型与决策边界。
- [FashionMNIST Classifier](projects/fashion_mnist_classifier/README.md)：真实图片 MLP、混淆矩阵、错误图片、保存与推理。真实数据下载必须显式触发，自动测试使用合成数据。
- 练习严格模式全部通过；能独立解释输入/输出 shape、训练梯度、验证模式和样本加权统计。

## 测试
从仓库根目录运行：
```bash
python -m pytest phase3_deep_learning/section07_pytorch_fundamentals
python -m pytest phase3_deep_learning/section07_pytorch_fundamentals -m exercise
python -m pytest phase3_deep_learning/section07_pytorch_fundamentals -m exercise --strict-exercises
```
TODO 的 XFAIL 表示未完成，不代表答案正确。项目不使用练习函数。

## 常见错误与 Debug
- loss.backward 报非标量：先确定损失怎样聚合；不要凭空传全 1 梯度掩盖目的。
- .grad 为 None：检查叶子节点、requires_grad、detach/no_grad；不要用 torch.tensor(x) 意外切断图。
- 验证 loss 异常：检查 eval/no_grad、损失分母、最后一个短 batch 和数据划分。
- 设备不一致：打印模型、输入和标签的 device；先在 CPU 完整跑通。
- 一直重复累积梯度：检查 zero_grad 的位置，区分有意的累积与未清理。

## 官方资料
- [基础教程](https://pytorch.org/tutorials/beginner/basics/intro.html)
- [Tensor](https://pytorch.org/docs/stable/tensors.html)
- [Autograd](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
- [nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)
