# 验证记录

本记录明确区分已执行的验证与依赖受限的验证。当前环境为 Linux、Python 3.12.3。

## 已执行

- 从本地包缓存安装 NumPy、Pillow、Matplotlib、pytest、ruff 和 PyYAML。
- `python -m pip install -e . --no-build-isolation --no-deps`：editable 构建和安装成功。
- `python -m pip wheel . --no-build-isolation --no-deps`：普通 wheel 构建成功；检查确认包含机器学习 YAML 配置、文本样例、CSV/JSON 样例和模块入口，且不含测试或字节码。
- `python scripts/generate_datasets.py --only core`：生成 1010 条用户记录、101 条商品记录、10100 条订单记录（含重复记录），以及房价、向量、回归、图片、文本和训练日志。
- `python scripts/smoke_projects.py --core`：八个核心项目的命令行流程全部通过。覆盖文件工具的读取、dry-run 与写入，六种图片操作，Batch/Mini-batch 回归、向量检索、文本分析、数据检查/清洗与训练日志对比；输出在临时目录中验证后清理。
- `ruff check .`、`ruff format --check .`、Python 编译检查。

最终核心测试结果：**207 passed、222 xfailed、6 deselected**。`--core` 明确取消选择三个依赖 sklearn 的数据生成用例，以及电商、EDA、机器学习的三个 CLI 导入用例；依赖完整数据科学环境的 Section 执行测试不属于此子集。TODO 的 xfail 表示练习尚未实现，不能计入已完成题目。

另用四个隔离 pytest 子进程验证反馈策略：原始骨架记为 xfail，错误返回值正常失败，已写入代码后主动抛 NotImplementedError 正常失败，严格模式中的骨架正常失败。安装后也从 `/tmp` 成功运行 `python -m dataset_inspector`，确认入口不依赖恰好处于源码目录。

本地核心依赖版本：NumPy 2.5.4、Pillow 12.3.0、Matplotlib 3.11.2、pytest 9.1.1、ruff 0.16.5、PyYAML 6.0.3。未验证所有允许版本的组合。

## 环境限制与待执行验证

当前终端无法联网访问包源，缓存缺少 pandas、scikit-learn、joblib、pytest-cov 及相关依赖。因此 `python -m pip install -e ".[dev]"` 未能完成；这与 editable 构建本身成功是两件不同的事。

已尝试全量测试入口 `python scripts/run_all_tests.py -q --tb=short -r fE`。收集阶段报告 10 个模块导入错误，原因是缺少 pandas、sklearn 或 joblib；没有把这些错误改为 skip 或 xfail。Pandas 练习、电商分析、部分 Matplotlib 练习、EDA、Scikit-learn 练习和完整机器学习项目尚未完成运行验证。覆盖率命令也尚未验证。

在依赖完整的环境中还需要执行：

```bash
python -m pip install -e ".[dev]"
python scripts/generate_datasets.py
python scripts/run_all_tests.py
python scripts/smoke_projects.py
python -m pytest -m "not exercise" --cov=phase1_python_programming --cov=phase2_data_science --cov-report=term-missing
```

当前环境可重复运行的明确子集：

```bash
python scripts/run_all_tests.py --core -q -r fE
python scripts/smoke_projects.py --core
```

`--core` 是显式选择，仅执行标准库/NumPy/Matplotlib 核心测试，保留整个仓库的静态结构检查，并排除依赖 Pandas/Scikit-learn 的执行路径。默认命令仍执行全量测试。
