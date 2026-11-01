# 开发规范

Python ≥3.11，UTF-8 编码，函数/模块 snake_case，类 PascalCase。公共接口提供类型提示和 docstring，先约定输入输出、错误类型、数据形状与缺失策略，再写实现。

函数只做一件主要工作，I/O 与变换分开；优先 pathlib、上下文管理器、标准库数据结构。输入数据默认不修改，返回独立结果；需要原地行为时必须在契约中说明。大文件逐行或分块处理，生成器应支持一次性迭代器。

NumPy 避免逐元素 Python 循环，允许按 mini-batch 或查询块循环；谨慎处理 dtype、shape、axis、零向量和数值溢出。使用局部 default_rng，不依赖全局随机状态。浮点测试使用 assert_allclose/approx。

Pandas 明确连接基数，使用 validate 防止无意放大行数；说明去重保留规则、缺失填充依据和异常值阈值。图形使用 Figure/Axes API，设置标题和坐标，保存后关闭。

机器学习先划分数据，预处理器放入 Pipeline 后再做交叉验证和搜索，避免每折或测试集信息泄漏。分类分层划分，按训练集 CV 选择最终模型，留出测试集用于最终报告。joblib 保存整个 Pipeline，而不是只有估计器。

文件变更默认 dry-run，先完整校验再执行；不覆盖目标文件。CLI 使用 argparse，错误返回非零退出码，logging 写入 stderr。可重建的报告、数据生成产物允许显式指定目录后重建。

pytest 测试独立使用 tmp_path，不能依赖上个测试产生的数据；重要函数覆盖正常、空输入与异常。每个练习至少三个参数用例，项目使用已知结果、梯度有限差分、序列化往返和数据泄漏检查等验证行为。运行 `ruff check .` 和 `ruff format --check .`。
