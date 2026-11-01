# Dataset Cleaning Pipeline

## 项目目标与需求

把缺失值填充、去重、类型转换、列筛选设计成独立函数，通过 CleaningPipeline 自由组合。

## 输入数据

带表头 CSV；--fill 是列到填充值的 JSON 对象；--types 支持 int/float/str。转换失败会报告错误，输入不被修改。

## 文件结构

src/cleaning_pipeline.py 包含纯函数、组合类、CSV 输入输出与 argparse 入口。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase1_python_programming.section02_python_engineering.projects.dataset_cleaning_pipeline.src.cleaning_pipeline --input phase1_python_programming/section02_python_engineering/projects/dataset_inspector/examples/sample.csv --output datasets/processed/cleaned.csv --fill '{"salary":"0"}' --types '{"age":"int","salary":"float"}' --columns age salary
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

cleaned.csv；datasets/processed/cleaning_comparison.json 提供 before/after 完整统计。输出 CSV 已存在时拒绝覆盖。

## 验收标准

可独立组合步骤；不修改传入记录；保留表头处理空数据；类型转换可测；统计前后行数和缺失变化。

```bash
python -m pytest phase1_python_programming/section02_python_engineering/projects/dataset_cleaning_pipeline/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
