# File Toolkit

## 项目目标与需求

实现递归扫描、SHA-256、重复文件发现、CSV 合并、JSON 标准化与安全批量重命名。

## 输入数据

UTF-8 CSV/JSON 或本地目录。CSV 表头和行宽必须一致；JSON 递归排序键、去字符串首尾空白；重复文件依据内容摘要。

## 文件结构

src/file_toolkit/operations.py 提供功能，cli.py 提供 argparse 入口。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli scan datasets/generated/ecommerce
python -m phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli hash datasets/generated/sample.txt
python -m phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli duplicates datasets/generated/ecommerce
python -m phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli merge datasets/generated/ecommerce/users.csv datasets/generated/ecommerce/users.csv --output datasets/processed/merged_users.csv
python -m phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli normalize datasets/generated/manifest.json --output datasets/processed/normalized.json
python -m phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli rename datasets/generated --mapping '{"sample.txt":"sample_renamed.txt"}'
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

stdout 为 JSON 结果或执行计划；stderr 记录操作日志。写操作默认 dry-run，需要 --apply 才写入。

## 验收标准

先验证完整计划再修改；拒绝路径越界、目标覆盖、重复目标、目录、符号链接与交换重命名；合并/标准化拒绝已存在输出。

```bash
python -m pytest phase1_python_programming/section02_python_engineering/projects/file_toolkit/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
