# Exploratory Data Analysis Report

## 项目目标与需求

复用 Section 04 清洗和分析结果，绘制年龄、城市、价格、类别销售、月销售、用户消费、相关性、箱线异常八种图。

## 输入数据

Section 04 生成的三张 CSV，由本项目调用相同清洗函数后绘图；无需先运行电商报告命令。

## 文件结构

src/eda.py 提供 generate_report 与 CLI，tests/test_eda.py 验证报告和八张 PNG。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase2_data_science.section05_matplotlib.projects.exploratory_data_analysis.src.eda
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

datasets/processed/eda/ 下 8 张 PNG 与 eda_report.md，报告为每张图提供解释和局限。

## 验收标准

使用 Figure/Axes API，标题/坐标完整；在无显示器环境保存；生成图片后关闭；每次执行结果结构一致。

```bash
python -m pytest phase2_data_science/section05_matplotlib/projects/exploratory_data_analysis/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
