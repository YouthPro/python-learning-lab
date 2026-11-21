# Phase 3 学习指南

## 前提与路线
完成Phase1/2的工程、数组、数据切分和评估，再进入07 Tensor→Autograd→MLP，08 Dataset→CNN→迁移，09配置→日志→Checkpoint→毕业工程。每节先完成练习严格测试，再解释项目中的对应设计。每题契约记录在[Phase3 manifest](phase3_exercise_manifest.json)，每题的shape/dtype/图在catalog中。

## 每次练习
1. 在纸上写Input/Output Shape、dtype、device和是否需要梯度。
2. 画计算图/推导梯度，先做最小输入和边界。
3. 实现TODO，仅用CPU运行单题pytest；浮点使用assert_close。
4. 解释为什么需要zero_grad、eval与no_grad，各控制什么。
5. 确认严格模式通过，不能把XFAIL当作完成。

## 项目实践
先跑离线synthetic模式检查工程，再显式下载真实数据做业务指标。单机MLP默认6000条；图片pipeline提供确定性PNG；CNN和迁移对比输出实际结果而不是预设分数。为每个实验选择不同输出目录，不使用test选择模型。

## 毕业项目核对
训练CSV/JSONL、best/latest、独立预测、模型切换、配置错误、数据指纹变化、连续训练与恢复训练对照均需检查。固定CPU与workers=0作为复现基线，再单独测GPU/多worker；依赖版本与硬件变化可能改变结果。

## Debug清单
- Shape从[N,C,H,W]逐层记录；输出[N,K]，CE标签[N] long。
- 错误损失不下降：确认optimizer含trainable参数、无重复softmax、无错误detach、学习率合适。
- 内存增长：日志存标量，预测不保留图，绘图后close。
- 预测不一致：检查RGB/灰度、resize和Normalize，与checkpoint预处理保持一致。
- 恢复不同：检查RNG、shuffle generator、scheduler、early stopper及optimizer，而不仅model。

## 最终验收和进阶
阶段验收见[Phase3 README](../phase3_deep_learning/README.md)。可选继续TensorBoard、Profiler和文本Embedding/LSTM；不要求Transformer，不引入高级训练框架。真实性能结论要独立重复、记录硬件，不能把synthetic smoke当作FashionMNIST或ImageNet效果。
