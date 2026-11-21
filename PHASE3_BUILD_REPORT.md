# Phase 3 构建与验收报告

验收日期：2026-11-03。工作目录：`/home/ai_infra/projects/python-learning-lab`。

## 交付内容

已在现有仓库增量追加 Phase 3，包含 43 道练习骨架、130 个练习参数用例、6 个可运行参考项目，以及章节说明、题目目录、学习指南和安装说明。没有提供练习题的完整答案。项目与练习实现相互独立，项目不会导入未完成的 TODO。

| Section | 练习 | 参考项目 | 项目测试用例 |
|---|---:|---|---:|
| 07 PyTorch Fundamentals | 18 | MLP Classifier、FashionMNIST Classifier | 6 |
| 08 Data Pipeline & Model Architecture | 15 | Image Dataset Pipeline、CNN Image Classifier、Transfer Learning Classifier | 12 |
| 09 Deep Learning Engineering | 10 | PyTorch Training Framework | 30 |

全部练习提供类型标注、函数/类签名、TODO、Hint、Input Shape、Output Shape、Expected dtype、梯度与计算图约定，每题至少三个测试用例。Autograd 五题另有简短的梯度过程说明。项目提供参考实现、README、任务拆分、运行命令、离线测试和验收标准。

入口：[阶段说明](phase3_deep_learning/README.md)、[学习指南](docs/phase3_learning_guide.md)、[总路线](docs/roadmap.md)。题目清单为 [phase3_exercise_manifest.json](docs/phase3_exercise_manifest.json)。

## 原有仓库检查与保护

开发前检查了目录、根 README、pyproject.toml、根 conftest、Phase 1/2 测试、包发现和已有 `dataset_inspector` 模块别名方式。沿用 setuptools、可编辑安装、pytest importlib 导入和现有精确 TODO 识别机制。

开始时仓库已有未提交修改，涉及 Section 01 练习、评分器、根配置及说明文件。本次没有回退这些修改；Phase 1/2 的 121 个原有文件（包含当时已有的未跟踪文件）均与开发前 SHA-256 一致。逐文件记录见 [legacy_integrity.json](docs/phase3_validation/legacy_integrity.json)。Git 中原有 Phase 1 文件的修改状态不代表本次修改了它们。

根目录必要整合包括：

- pyproject.toml 追加 `deep-learning` 可选依赖、Phase 3 包发现、YAML/演示图片打包声明和测试路径；保留原有基础依赖、dev/notebook 组与 Advanced 标记。
- 默认 pytest 排除 exercise；显式 `-m exercise` 运行练习。保留严格练习模式和原有 Section 01 评分器的收集行为。显式指定练习 tests 路径也保留原行为，显式 `-m` 优先。
- 根仓库结构检查分别验证原有 11 个项目和新增 6 个项目，没有移除原有数量断言。新增 47 项 Phase 3 静态契约检查。
- README、路线图、忽略规则和统一测试入口做增量更新。没有增加 Web UI、数据库、Docker 或高级训练框架。

初始虚拟环境缺少 pandas/scikit-learn/PyTorch 等依赖，基线测试有 10 个收集错误。安装已有依赖和新增可选组后完成下列验收；没有用 skip 掩盖缺依赖。

## 六个项目的实现

### Section 07

MLP 项目使用 NumPy 生成默认 6000 条非线性二维数据，固定种子并划分 train/validation/test，提供 TensorDataset、DataLoader、可配置网络/激活/优化器/学习率、样本加权训练统计、验证选择 best、模型重载、训练曲线与决策边界。

FashionMNIST 项目使用 torchvision 数据与 transforms，提供 MLP、训练/验证/测试、混淆矩阵、错误图片、最优参数保存和重载推理。`--download` 才允许下载；`--synthetic` 可离线运行完整流程。

### Section 08

图片管线使用自定义 PIL Dataset，支持排序类别映射、图片完整解码与损坏检查、可复现 split 清单、独立 train/eval transforms、Resize/Crop/Flip/Normalize、DataLoader 和类别不平衡统计。包含生成脚本与 6 张可重复生成的演示图片；生成器不会删除自备文件。

CNN 项目分离 ConvBlock、模型与训练入口，包含 BatchNorm/ReLU/MaxPool/Dropout/AdaptivePool。比较 MLP/CNN、卷积层数、batch size、学习率和 Dropout，输出实际实验 CSV/Markdown、混淆矩阵及错误样本。真实 FashionMNIST 下载仍需要显式参数。

迁移项目使用 torchvision ResNet18，支持 A（只训练 fc）、B（layer4+fc）、C（全部微调），比较验证准确率、完整 fit 耗时和参数量。每个策略从相同随机种子/初始权重开始，重新创建 optimizer，冻结层的 BatchNorm 统计量也保持固定。A 与 B/C 的学习率配置不同，报告明确记录这些差异，不将其当作单变量实验。

支持 Synthetic、FashionMNIST、CIFAR10 与自定义类别目录。`--download-data` 和 `--pretrained` 分别控制数据/权重下载；加载已保存模型时先构建 `weights=None` 结构，再载入 state_dict，不联网。真实预训练使用 224 RGB、ImageNet Normalize，验证采用 Resize256/CenterCrop224；灰度输入先转换 RGB。

### Section 09 毕业项目

`training_framework` 提供 config、seed、datasets、models、engine、utils、CLI，支持 Synthetic/ImageFolder、MLP/CNN、原生训练和验证、Adam/SGD、Step/Cosine/Plateau Scheduler、Early Stopping、梯度裁剪、梯度累积、CSV/JSONL、学习曲线和独立单图预测。

Checkpoint 原子写入 best/latest，保存模型、optimizer、scheduler、AMP scaler、epoch、最优指标、early stopping、配置、类别/预处理、数据指纹、history、Python/NumPy/PyTorch 随机状态及 DataLoader Generator 状态。显式 `weights_only=True`、CPU map_location 加载，不序列化整个模型对象。NumPy RNG 状态转换为安全加载支持的张量和基本类型。

恢复训练从 epoch+1 开始，校验训练配置与数据内容/划分，允许改变总 epoch、输出路径、device 和 threads。日志以 checkpoint history 重建，避免重复 epoch 或遗留半行。无效恢复请求不会改写原 split 清单。训练输出目录已有 checkpoint 时要求显式 resume 或新目录。

设备默认 CPU，auto 检测 CUDA/MPS；AMP 仅在选中且可用的 CUDA 上启用。梯度累积按实际样本数归一化，处理最后不足窗口和短 batch，AMP 先 unscale 再 clip。

## 实际环境与兼容性调整

本次使用 Python 3.12.3、PyTorch 2.15.0+cpu、Torchvision 0.29.2+cpu，系统为 WSL2 Ubuntu。完整版本清单见 [phase3_build_evidence.json](docs/phase3_build_evidence.json)。`pip check` 通过。

不固定 CUDA 版本。README 要求先用 [PyTorch 官方安装选择器](https://pytorch.org/get-started/locally/)安装兼容 Torch/Torchvision，再安装 `.[dev,deep-learning]`。本环境使用官方 CPU wheel；未下载真实数据集或预训练权重。

明确的 API/行为约定：

- 标准化练习使用总体标准差 `correction=0`，避免长度为 1 时产生 NaN；零向量余弦相似度定义为 0。
- 使用现代 `weights=`、显式安全 checkpoint 加载和 `torch.amp` API，避免旧版 `pretrained=True`/CUDA 写死方式。
- 32px ResNet 训练末批若仅剩一张且特征图为 1×1，BatchNorm 无法估计方差；迁移项目省略该单张训练尾样本，验证不丢样本。该行为在项目 README 说明。
- `training_framework` 使用与原仓库一致的顶层模块别名，实际代码仍在指定的 `src/training_framework` 目录。共享原生训练工具放在 Phase 3 common 内，避免复制六套相同实现。
- 保持既有 TODO 的精确 XFAIL 机制。严格模式会把未完成练习视为失败；项目实现错误和已填写练习的断言失败不会转为 TODO。

## 验收结果

| 检查 | 实际结果 |
|---|---|
| 最终默认全仓库 pytest | **363 passed，495 deselected，0 failed** |
| 单独 Phase 1/2 项目回归 | **109 passed** |
| 新增项目核心测试 | **48 passed**，包括毕业项目 30 项 |
| 新增题目清单/静态契约 | **47 passed** |
| 旧 Section 01 评分器回归 | **28 passed** |
| Phase 3 练习测试 | **130 XFAIL**，均为要求保留的 TODO；不计作解题完成 |
| 严格练习模式 | 第一处 TODO 正常失败，退出码 1，符合预期 |
| 六项目离线 CLI 验收 | **22 条命令全部退出码 0**，子进程禁止互联网访问 |
| Wheel 打包与导入 | **65 个模块全部来自解包 wheel**，3 份配置及 6 张演示图齐全，MLP/CNN shape 正确 |
| Ruff | 新增代码和本次触及的根 Python 文件检查通过，103 个文件格式检查通过 |
| Phase 3 实现行覆盖率 | **85.27%（932/1093）**；排除题目骨架、测试和 conftest，不代表 CUDA 路径已验证 |
| Phase 1/2 文件完整性 | **121/121 SHA-256 不变** |

以上数量有包含关系，不应直接相加。默认全仓库结果有 31 条警告：30 条来自原有 Pandas 测试的前向兼容提示，1 条为 Linux 多线程环境下 DataLoader fork 提示；没有测试失败。

端到端验收实际完成：6000 条二维数据训练、SGD/不同结构入口、Fashion/CNN 合成图片训练、CNN 六组比较、真实随机初始化 ResNet18 的 A/B/C 训练与单图推理、框架 MLP 训练→恢复→验证→灰度预测，以及 CNN 与自定义 RGB 图片训练→预测。二维合成数据测试准确率为 1.0，这不代表 FashionMNIST/CIFAR10 或真实迁移效果。

恢复正确性测试对比连续 3 epoch 与 1 epoch 后恢复到 3 epoch：模型权重以 `rtol=0, atol=0` 逐项相等，loss、accuracy、学习率、best epoch 和 early stopping 状态一致。另验证短 batch 累积等价性、损坏日志修复、安全加载拒绝模块 pickle 和不合法配置报错。

## 复查方式与证据

在已安装依赖的仓库根目录：

```bash
python -m pytest
python -m pytest phase1_python_programming phase2_data_science -m 'not exercise'
python -m pytest phase3_deep_learning tests/test_phase3_contract.py -m 'not exercise'
python -m pytest phase3_deep_learning -m exercise
python -m pytest --cov --cov-config=phase3_deep_learning/coverage.ini
python scripts/smoke_phase3.py
```

CLI 验收默认创建独立临时输出目录；显式 `--output` 应指定新路径。模型与图表放在该目录，避免将训练产物混入源码。

持久化记录位于 [docs/phase3_validation](docs/phase3_validation)：JUnit、测试日志、覆盖率、版本、Ruff、wheel 导入检查、22 条命令及 stdout/stderr、文件完整性记录。汇总入口为 [phase3_build_evidence.json](docs/phase3_build_evidence.json)。本次训练产物保留在 `/tmp/python-lab-phase3-smoke-final`，临时目录清理后可重新执行脚本生成。

六个项目 README 的离线命令及 CLI 参数已实际检查；下载命令通过入口和参数检查，没有运行联网训练。毕业项目从其项目目录直接执行文档中的 `python -m training_framework.cli ...`，验证了安装后的导入方式。

## 未完成事项与验证边界

核心交付已实现并通过离线 CPU 验收。以下保留为明确的可选扩展或后续实际实验：

- 43 道练习按要求保持未实现，130 个 XFAIL 是学习任务，不是已通过的练习答案。
- TensorBoard、PyTorch Profiler、可选文本分类未实现，不纳入核心交付。
- 没有 CUDA/MPS 硬件，未执行真实 GPU、MPS 或 AMP 训练；已实现设备检测与 CPU 回退。
- 未下载 FashionMNIST/CIFAR10/预训练权重，未声称获得这些真实数据集的成绩或预训练迁移收益。
- 恢复支持 epoch 边界；不支持任意 batch 中断的精确续跑。位级复现仅在固定 CPU 环境的测试中验证，不保证跨硬件、依赖版本或 worker 策略一致。
- 当前实际运行环境为 Python 3.12，项目声明 Python 3.11+；未建立多 Python 版本 CI 矩阵。

官方 API 依据：[ResNet18](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html)、[保存和加载通用 Checkpoint](https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html)。各 Section README 提供对应官方学习资料。
