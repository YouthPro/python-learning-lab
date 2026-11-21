# cnn_image_classifier

可独立运行的参考项目，安装仓库 `.[dev,deep-learning]` 后从仓库根目录运行。

## 任务拆分与结构
1. 检查输入/标签与数据划分。
2. 实现并验证数据和模型模块。
3. 调用原生训练循环（不导入练习TODO）。
4. 保存产物，检查结果和边界。

`src/` 分离数据、模型与命令；`tests/` 为CPU离线测试；`scripts/` 存放相关生成入口。共享工具位于 `phase3_deep_learning/common/`。

## 模型与运行
输入[N,1,28,28]，输出[N,10] logits。ConvBlock包含Conv2d/BatchNorm/ReLU/MaxPool/Dropout，AdaptivePool支持不同空间尺寸。
```bash
python -m phase3_deep_learning.section08_data_pipeline_and_models.projects.cnn_image_classifier --synthetic --epochs 2 --output outputs/phase3/cnn_smoke
python -m phase3_deep_learning.section08_data_pipeline_and_models.projects.cnn_image_classifier --synthetic --compare --epochs 1 --output outputs/phase3/cnn_compare
# 显式真实数据下载：去掉 --synthetic，加 --download
```
--compare实际执行6组配置，逐项比较MLP/CNN、卷积深度、batch size、learning rate、dropout；生成comparison.csv/md和各自的模型、曲线、混淆矩阵及错误图。正常参数也可单独指定。合成指标不冒充FashionMNIST效果；按val选择权重，test不用于调参。
验收：所有层有梯度，输出shape正确，best/latest.pt可安全加载，混淆矩阵样本数正确，报告使用实际测量值。

## 测试
```bash
python -m pytest phase3_deep_learning/section08_data_pipeline_and_models/projects/cnn_image_classifier/tests
```
