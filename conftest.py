"""Recognize only untouched TODO bodies; assertion failures always remain failures."""

import ast
import math
import os
from pathlib import Path

import pytest

os.environ.setdefault("MPLBACKEND", "Agg")


def pytest_addoption(parser):
    parser.addoption("--strict-exercises", action="store_true", help="TODO 也视为测试失败")
    parser.addoption(
        "--run-advanced",
        action="store_true",
        help="Run Advanced Time Tests and Advanced Memory Tests",
    )
    parser.addoption(
        "--advanced-time-multiplier",
        type=float,
        default=1.0,
        help="Explicit hardware adjustment for advanced time limits",
    )


def pytest_configure(config):
    value = config.getoption("--advanced-time-multiplier")
    if not math.isfinite(value) or value <= 0:
        raise pytest.UsageError("--advanced-time-multiplier must be finite and positive")
    # Default pytest is project-only, but the existing grading subprocesses
    # and explicit exercise-test paths must still collect learner contracts.
    # An explicit -m/--markexpr always wins over this compatibility default.
    arguments = config.invocation_params.args
    explicit_marker = any(arg.startswith("-m") or arg.startswith("--markexpr") for arg in arguments)
    exercise_path = any(
        "tests" in Path(arg).parts
        and "projects" not in Path(arg).parts
        and any(part.startswith(("phase1_", "phase2_", "phase3_")) for part in Path(arg).parts)
        for arg in arguments
        if not arg.startswith("-")
    )
    assessment = config.getoption("--section01-results", default=None) is not None
    if (
        config.option.markexpr == "not exercise"
        and not explicit_marker
        and (exercise_path or assessment)
    ):
        config.option.markexpr = ""


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
