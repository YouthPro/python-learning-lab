# 学习路线

按 Section 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 进行。前两节只需 Python 基础；第二阶段依次引入数组、表格、可视化与传统机器学习。

| Section | 建议训练顺序 | 阶段成果 |
|---|---|---|
| 01 | 12 基础结构 → 10 标准库 → 8 函数与迭代器 | 流式文本分析 |
| 02 | 6 文件练习 → 异常与 logging → dataclass/组合/测试 | 三个工程项目 |
| 03 | 8 数组 → 3 广播 → 4 数值计算 | 图片处理、向量检索、手写回归 |
| 04 | 6 DataFrame → 4 清洗 → 5 分组变换 | 电商分析报告 |
| 05 | 5 基础图 → 3 高级图 | 电商 EDA 与模拟训练可视化 |
| 06 | 3 预处理 → 3 评估 → 2 模型选择 | 房价回归与二分类完整流程 |

每次以严格模式通过一组练习，再完成对应项目。训练速度由理解和测试结果决定，不以固定天数为约束。Section README 内维护勾选进度。完成 Phase 2 后应能解释数据泄漏、dtype/shape、数据质量策略、模型比较与报告局限。


## Phase 3：从 Tensor 到可恢复训练工程

| Section | 推荐顺序 | 阶段成果 |
|---|---|---|
| [07](../phase3_deep_learning/section07_pytorch_fundamentals/README.md) | 8 Tensor → 5 Autograd → 5 Training | 6000条MLP分类、真实FashionMNIST MLP |
| [08](../phase3_deep_learning/section08_data_pipeline_and_models/README.md) | 6数据 → 4 CNN → 5迁移 | 自定义图片Dataset、CNN对照、ResNet18 A/B/C |
| [09](../phase3_deep_learning/section09_deep_learning_engineering/README.md) | 2配置复现 → 5训练辅助 → 3 Checkpoint | 原生PyTorch Training Framework |

共43题、6项目。详见[阶段学习指南](phase3_learning_guide.md)。先离线CPU跑通，再显式下载真实数据；先通过练习严格测试，再阅读参考项目。毕业时能解释shape、梯度、数据泄漏、冻结/微调、模型选择及恢复训练状态。
