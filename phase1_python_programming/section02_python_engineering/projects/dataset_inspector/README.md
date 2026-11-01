# Dataset Inspector

## 项目目标与需求

使用 DatasetManager 组合读取、缺失值处理和统计，输出 JSON/Markdown 数据质量报告。

## 输入数据

带表头的 UTF-8 CSV 或对象列表 JSON。默认缺失标记为空串、NA、null、None 和实际 None/NaN；可通过 --missing-values 覆盖。

## 文件结构

src/dataset_inspector/manager.py、reporter.py、__main__.py；examples/ 包含小样例。仓库顶层 dataset_inspector 是安装后的模块入口。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m dataset_inspector --input phase1_python_programming/section02_python_engineering/projects/dataset_inspector/examples/sample.csv --output datasets/processed/inspection
python -m dataset_inspector --input phase1_python_programming/section02_python_engineering/projects/dataset_inspector/examples/sample.json --strategy fill --fill-value unknown --output datasets/processed/inspection_json
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

summary.json 和 summary.md；stdout 展示行列数、重复行、每列缺失计数/比例与列统计。

## 验收标准

数值列输出 mean/median/min/max/样本 std（单值 std=0）；类别列输出 unique_values/top_categories；keep/drop/fill 策略明确；空表能统计。

```bash
python -m pytest phase1_python_programming/section02_python_engineering/projects/dataset_inspector/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
