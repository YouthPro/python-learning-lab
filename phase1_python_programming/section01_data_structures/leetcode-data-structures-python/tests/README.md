# 本地测试

在项目根目录使用 Python 3.11 或更新版本运行语法和导入检查。

```bash
python -m compileall -q common sections

python - <<'PY'
from importlib import import_module
from pathlib import Path

problems = sorted(Path("sections").glob("*/*/p*.py"))
assert len(problems) == 141, len(problems)

for path in problems:
    import_module(".".join(path.with_suffix("").parts))

print(f"已独立导入 {len(problems)} 个题目模块")
PY
```

Section 目录名以数字开头，本地用例通过 `importlib.import_module` 导入。比如第 26 题的模块路径为 `sections.01_array.easy.p0026_remove_duplicates_from_sorted_array`。链表和树的用例可从 `common.nodes` 导入节点。

写好某题后，可在 `tests/` 下新增 `test_*.py`，用 `unittest.TestCase` 覆盖官方样例和边界输入，然后运行以下命令。

```bash
python -m unittest discover -s tests -p 'test_*.py'
```
