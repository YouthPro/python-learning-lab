"""Recognize only untouched TODO bodies; assertion failures always remain failures."""

import ast
import os
from pathlib import Path

import pytest

os.environ.setdefault("MPLBACKEND", "Agg")


def pytest_addoption(parser):
    parser.addoption("--strict-exercises", action="store_true", help="TODO 也视为测试失败")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if item.config.getoption("--strict-exercises") or call.excinfo is None:
        return
    if call.excinfo.type is not NotImplementedError or report.when != "call":
        return
    frame = call.excinfo.traceback[-1]
    path = Path(str(frame.path))
    if "exercises" not in path.parts:
        return
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                body = body[1:]
            if (
                len(body) == 1
                and isinstance(body[0], ast.Raise)
                and node.lineno <= frame.lineno + 1 <= node.end_lineno
            ):
                report.outcome = "skipped"
                report.wasxfail = "未完成的练习 TODO；使用 --strict-exercises 查看失败"
                break
