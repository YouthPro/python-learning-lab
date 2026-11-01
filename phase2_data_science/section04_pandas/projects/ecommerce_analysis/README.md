# E-commerce Data Analysis

## 项目目标与需求

拆分数据加载、清洗、关联分析和报告输出，完成销售额、用户消费、热门商品、城市与注册月份购买行为分析。

## 输入数据

users.csv: user_id,age,gender,city,register_date；products.csv: product_id,product_name,category,price；orders.csv: order_id,user_id,product_id,quantity,order_date。默认 1000 用户、100 商品、10000 订单，另加 1% 重复记录并注入缺失和异常。

## 文件结构

src/data_loader.py、cleaning.py、analysis.py、reporting.py；main.py；data/；reports/；tests/。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase2_data_science.section04_pandas.projects.ecommerce_analysis.main
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

项目 reports/ 下生成 data_quality_report.md、sales_analysis.csv（月销售额）、customer_analysis.csv（全体用户消费）、product_analysis.csv（按销量排序）；另外输出类别、城市、注册月份、清洗数据与 summary.json。

## 验收标准

关联使用 many_to_one 校验；异常和缺失处理有明确策略；金额一致性、Top 10、用户均值可验证；输入不被修改；无 Notebook 依赖。

```bash
python -m pytest phase2_data_science/section04_pandas/projects/ecommerce_analysis/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
