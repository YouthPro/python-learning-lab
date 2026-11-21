# Python Learning Lab

面向已掌握 Python 基础语法、准备学习深度学习与数据处理的学习者。通过函数练习与完整项目，训练编程、工程、NumPy、Pandas、Matplotlib 和 Scikit-learn；新增 Phase 3 PyTorch 深度学习；Phase 1 / Phase 2 的内容保留。核心自动测试不依赖 Notebook、GPU 或在线数据下载。

## 安装

需要 Python 3.11+。从本仓库根目录运行：

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python scripts/generate_datasets.py
```

也可通过 `python -m pip install -r requirements.txt` 安装。可选 Notebook 环境为 `python -m pip install -e ".[dev,notebook]"`。主要依赖为 numpy、pandas、matplotlib、scikit-learn、Pillow、joblib；机器学习配置使用 PyYAML。开发工具为 pytest、pytest-cov、ruff。

依赖安装需要可用的软件包源；安装后所有基础数据和项目均离线运行。生成数据默认 seed=42，可通过 `--seed` 修改。同一种子和依赖版本重复生成内容一致；不会读取或修改 datasets/raw/ 中的自备数据。

## 学习路线

| 阶段 | Section | 练习 | 完整项目 |
|---|---|---:|---|
| Phase 1 | [01 数据结构与标准库](phase1_python_programming/section01_data_structures/README.md) | 30 | Text Analyzer |
| Phase 1 | [02 工程与文件处理](phase1_python_programming/section02_python_engineering/README.md) | 6 + 3 个工程专题 | File Toolkit、Dataset Inspector、Dataset Cleaning Pipeline |
| Phase 2 | [03 NumPy](phase2_data_science/section03_numpy/README.md) | 15 | Image Processor、Vector Similarity、Linear Regression |
| Phase 2 | [04 Pandas](phase2_data_science/section04_pandas/README.md) | 15 | E-commerce Analysis |
| Phase 2 | [05 Matplotlib](phase2_data_science/section05_matplotlib/README.md) | 8 | EDA Report、Training Visualizer |
| Phase 2 | [06 Scikit-learn](phase2_data_science/section06_sklearn/README.md) | 8 | Regression + Classification Workflow |
| Phase 3 | [07 PyTorch Fundamentals](phase3_deep_learning/section07_pytorch_fundamentals/README.md) | 18 | MLP、FashionMNIST |
| Phase 3 | [08 Data Pipeline & Models](phase3_deep_learning/section08_data_pipeline_and_models/README.md) | 15 | Image Pipeline、CNN、Transfer Learning |
| Phase 3 | [09 Deep Learning Engineering](phase3_deep_learning/section09_deep_learning_engineering/README.md) | 10 | PyTorch Training Framework |

合计 125 道指定练习、3 个工程专题、17 个完整项目。每道题的名称、难度、知识点、签名、描述、两个以上示例和边界见对应 exercise_catalog.md；exercises/ 中保留 TODO，不提供练习答案。projects/ 是可运行的参考项目，建议完成练习后再阅读。

## 运行测试

一条命令运行所有测试（脚本会自动定位仓库根目录）：

```bash
python scripts/run_all_tests.py
```

当前交付环境的依赖限制和实际执行结果见 [验证记录](docs/validation.md)。仅运行标准库、NumPy、Matplotlib 的明确子集可用 `python scripts/run_all_tests.py --core`；完整项目 CLI 验证为 `python scripts/smoke_projects.py`（同样支持 `--core`）。

Section 01 另提供 30 组 **Advanced Time Tests** 和 **Advanced Memory Tests**。运行 `python scripts/assess_section01.py --problem two_sum` 可获得正确性、时间/限制、内存/限制报告；省略 `--problem` 评估全部 30 题。逐题限制与测量方法见 [性能评估指南](docs/section01_performance.md)。

默认 `pytest` 仅运行项目与仓库检查（排除 exercise）；`pytest -m exercise` 单独运行练习。未实现的练习使用精确骨架识别，记为 **xfail**，并非已完成。仅当异常来自 exercises/ 下仍只有 docstring 和 raise 的函数体时识别为 TODO；修改为实际实现后，断言失败或异常会正常报错。项目不允许用 TODO 代替实现。

```bash
# 验收学习进度：未完成练习直接失败
python scripts/run_all_tests.py --strict-exercises
# 只验证完整项目与仓库质量
python scripts/run_all_tests.py -m "not exercise"
# 单题反馈
python -m pytest phase1_python_programming/section01_data_structures/tests/test_basic_structures.py -k two_sum
# 工程检查
ruff check .
ruff format --check .
python -m pytest -m "not exercise" --cov=phase1_python_programming --cov=phase2_data_science --cov-report=term-missing
```

## 项目入口

所有项目都有独立 README，包含输入、运行命令、输出与验收标准；下列模块均可从根目录执行 `python -m 模块 --help`。

| 项目 | 模块 |
|---|---|
| [Text Analyzer](phase1_python_programming/section01_data_structures/projects/text_analyzer/README.md) | `phase1_python_programming.section01_data_structures.projects.text_analyzer.src.text_analyzer.cli` |
| [File Toolkit](phase1_python_programming/section02_python_engineering/projects/file_toolkit/README.md) | `phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli` |
| [Dataset Inspector](phase1_python_programming/section02_python_engineering/projects/dataset_inspector/README.md) | `dataset_inspector` |
| [Cleaning Pipeline](phase1_python_programming/section02_python_engineering/projects/dataset_cleaning_pipeline/README.md) | `phase1_python_programming.section02_python_engineering.projects.dataset_cleaning_pipeline.src.cleaning_pipeline` |
| [Image Processor](phase2_data_science/section03_numpy/projects/image_processor/README.md) | `phase2_data_science.section03_numpy.projects.image_processor.src.image_processor` |
| [Vector Similarity](phase2_data_science/section03_numpy/projects/vector_similarity/README.md) | `phase2_data_science.section03_numpy.projects.vector_similarity.src.vector_similarity` |
| [NumPy Regression](phase2_data_science/section03_numpy/projects/linear_regression/README.md) | `phase2_data_science.section03_numpy.projects.linear_regression.main` |
| [Ecommerce Analysis](phase2_data_science/section04_pandas/projects/ecommerce_analysis/README.md) | `phase2_data_science.section04_pandas.projects.ecommerce_analysis.main` |
| [EDA Report](phase2_data_science/section05_matplotlib/projects/exploratory_data_analysis/README.md) | `phase2_data_science.section05_matplotlib.projects.exploratory_data_analysis.src.eda` |
| [Training Visualizer](phase2_data_science/section05_matplotlib/projects/training_visualizer/README.md) | `phase2_data_science.section05_matplotlib.projects.training_visualizer.src.training_visualizer` |
| [ML Workflow](phase2_data_science/section06_sklearn/projects/machine_learning_workflow/README.md) | `phase2_data_science.section06_sklearn.projects.machine_learning_workflow.main` |

File Toolkit 的写操作默认 dry-run，添加 `--apply` 后才执行；重命名、合并等操作拒绝覆盖。清洗项目同样拒绝覆盖已有输出 CSV，重复示例时请选择新路径。分析报告、训练曲线等可重建产物允许重新生成。

## 目录与说明

- docs/：[路线图](docs/roadmap.md)、[学习方法](docs/learning_guide.md)、[代码规范](docs/coding_conventions.md)、[验证记录](docs/validation.md)。
- datasets/raw/：自备原始数据；generated/：固定种子的模拟数据；processed/：清洗与输出产物。
- 每个 Section：README.md、exercise_catalog.md、exercises/、tests/、projects/。
- scripts/：离线数据生成与统一测试入口；tests/：仓库结构和数据生成测试。

验收时区分“项目功能测试通过”“未完成练习 xfail”和“严格练习测试通过”。项目实现与测试不依赖练习答案。

## Phase 3 安装与验收

深度学习依赖作为可选组追加，原有基础依赖和Phase1/2文件不重构。先使用[PyTorch官方安装选择器](https://pytorch.org/get-started/locally/)选择兼容Torch/Torchvision，再安装：

```bash
python -m pip install -e '.[dev,deep-learning]'
pytest
pytest -m exercise
pytest --cov
```

Linux纯CPU可先使用 `python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu`；不固定CUDA版本。只安装基础环境时仍可显式运行 `pytest phase1_python_programming phase2_data_science`；完整默认测试需可选组，缺依赖不会静默skip。

[Phase3学习指南](docs/phase3_learning_guide.md) · [完整阶段说明](phase3_deep_learning/README.md)。运行六个项目的离线命令验收：`python scripts/smoke_phase3.py`。所有真实数据与预训练权重下载都需显式flag，synthetic指标不代表真实数据效果。工程默认CPU，auto检测CUDA/MPS，AMP仅兼容CUDA。框架支持best/latest、CSV/JSONL、完整epoch边界恢复与单图预测。

实际创建与验证结果见 [PHASE3_BUILD_REPORT.md](PHASE3_BUILD_REPORT.md)。
