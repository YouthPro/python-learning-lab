"""Verify measurement boundaries, failure detection and actual submission grading."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from phase1_python_programming.section01_data_structures.assessment import engine, worker
from phase1_python_programming.section01_data_structures.assessment.cases import (
    BY_ID,
    CASES,
    MIB,
    select_cases,
)
from phase1_python_programming.section01_data_structures.assessment.engine import (
    ROOT,
    describe_metric,
    run_metric,
)
from phase1_python_programming.section01_data_structures.assessment.workloads import Workload


@pytest.mark.parametrize(
    "problems,ids",
    [(None, [c.id for c in CASES]), (["04", "two_sum"], ["04"]), (["30", "1"], ["01", "30"])],
)
def test_selection(problems, ids):
    assert [c.id for c in select_cases(problems)] == ids


@pytest.mark.parametrize("problem", ["31", "missing_function", "-1"])
def test_unknown_problem(problem):
    with pytest.raises(ValueError, match="Unknown"):
        select_cases([problem])


def test_all_problems_have_distinct_budgets_and_workloads():
    assert len(CASES) == 30
    assert len({c.id for c in CASES}) == len({c.name for c in CASES}) == 30
    for case in CASES:
        assert case.seconds > 0 and case.memory_mib > 0
        assert case.workload and case.expected_time and case.expected_space
        assert case.tests


def test_timing_is_median_and_does_not_trace_allocations(tmp_path, monkeypatch):
    moments = iter([0.0, 0.03, 1.0, 1.01, 2.0, 2.02])
    events = []

    def prepare(*args):
        events.append("prepare")

        def operation():
            assert not worker.tracemalloc.is_tracing()
            events.append("operation")
            return 7

        def validate(output):
            assert output == 7
            events.append("validate")

        return Workload(operation, validate)

    monkeypatch.setattr(worker, "make_workload", prepare)
    monkeypatch.setattr(worker.time, "perf_counter", lambda: next(moments))
    case = replace(BY_ID["04"], seconds=0.015)
    result = worker.measure(case, object(), "time", tmp_path)
    assert result["measured"] == pytest.approx(0.02)
    assert result["ratio"] == pytest.approx(4 / 3)
    assert result["status"] == "failed_limit"
    assert events == ["prepare", "operation", "validate"] * 3


@pytest.mark.parametrize("input_mib", [8, 12, 16])
def test_memory_excludes_preparation_and_validation_but_includes_output(
    tmp_path, monkeypatch, input_mib
):
    def prepare(*args):
        source = bytearray(input_mib * MIB)

        def operation():
            assert source[0] == 0
            return bytearray(4 * MIB)

        def validate(output):
            assert not worker.tracemalloc.is_tracing()
            assert len(output) == 4 * MIB
            # Deliberately large validation allocation must not count toward the peak.
            assert len(bytearray(16 * MIB)) == 16 * MIB

        return Workload(operation, validate)

    monkeypatch.setattr(worker, "make_workload", prepare)
    result = worker.measure(replace(BY_ID["04"], memory_mib=1), object(), "memory", tmp_path)
    assert result["status"] == "failed_limit"
    assert 4 * MIB <= result["measured"] < 4.1 * MIB
    assert result["ratio"] == pytest.approx(4, abs=0.1)
    assert len(result["samples"]) == 1


@pytest.mark.parametrize("metric", ["time", "memory"])
def test_wrong_stress_output_never_passes(tmp_path, monkeypatch, metric):
    def validate(value):
        assert value == "correct"

    monkeypatch.setattr(worker, "make_workload", lambda *args: Workload(lambda: "wrong", validate))
    result = worker.measure(BY_ID["04"], object(), metric, tmp_path, repeats=1)
    assert result["status"] == "wrong_answer"
    assert result["measured"] is not None
    assert "AssertionError" in result["detail"]


@pytest.mark.parametrize(
    "error,status",
    [
        (ValueError("bad"), "error"),
        (MemoryError(), "memory_guard"),
        (worker.MeasurementDeadline("deadline"), "timeout"),
    ],
)
def test_operation_errors_are_reported_and_tracing_stops(tmp_path, monkeypatch, error, status):
    def operation():
        raise error

    monkeypatch.setattr(
        worker, "make_workload", lambda *args: Workload(operation, lambda result: None)
    )
    result = worker.measure(BY_ID["04"], object(), "memory", tmp_path)
    assert result["status"] == status
    assert not worker.tracemalloc.is_tracing()


@pytest.mark.parametrize(
    "arguments",
    [
        {"time_multiplier": 0},
        {"time_multiplier": float("nan")},
        {"repeats": 0},
        {"wall_timeout": -1},
    ],
)
def test_invalid_measurement_settings(arguments):
    with pytest.raises(ValueError):
        run_metric(BY_ID["04"], "time", **arguments)


def test_parent_watchdog_does_not_invent_measurements(monkeypatch):
    def expire(*args, **kwargs):
        raise subprocess.TimeoutExpired("worker", 0.01)

    monkeypatch.setattr(engine.subprocess, "run", expire)
    result = run_metric(BY_ID["04"], "time", target_module="unused")
    assert result["status"] == "worker_timeout"
    assert result["measured"] is result["ratio"] is None
    assert "not measured" in describe_metric(result)


@pytest.mark.parametrize("kind", ["streaming", "eager", "hang"])
def test_real_worker_streaming_memory_and_timeout(tmp_path, monkeypatch, kind):
    if kind == "streaming":
        body = "with open(path,encoding='utf-8') as handle:\n        for line in handle: yield line.rstrip('\\r\\n')"
    elif kind == "eager":
        body = "return iter(path.read_text(encoding='utf-8').splitlines())"
    else:
        body = "while True: pass"
    module = "assessment_fixture_" + kind
    (tmp_path / f"{module}.py").write_text("def read_lines(path):\n    " + body + "\n")
    monkeypatch.setenv("PYTHONPATH", str(tmp_path) + os.pathsep + str(ROOT))
    result = run_metric(
        BY_ID["29"], "time" if kind == "hang" else "memory", target_module=module, wall_timeout=5
    )
    if kind == "streaming":
        assert result["status"] == "passed", result
        assert result["ratio"] <= 1
    elif kind == "eager":
        assert result["status"] == "failed_limit", result
        assert result["ratio"] > 10
    else:
        assert result["status"] in {"timeout", "worker_timeout"}, result
        if result["measured"] is not None:
            assert result["ratio"] > 1


CORRECT_TWO_SUM = """def two_sum(nums, target):
    seen = {}
    for j, number in enumerate(nums):
        if target-number in seen:
            return [seen[target-number], j]
        seen.setdefault(number, j)
    return []
"""


def isolated_checkout(path: Path):
    section = Path("phase1_python_programming/section01_data_structures")
    for name in ["assessment", "tests"]:
        shutil.copytree(
            ROOT / section / name,
            path / section / name,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
    shutil.copyfile(ROOT / "conftest.py", path / "conftest.py")
    shutil.copyfile(ROOT / "pyproject.toml", path / "pyproject.toml")
    shutil.copyfile(ROOT / section / "conftest.py", path / section / "conftest.py")
    exercises = path / section / "exercises"
    exercises.mkdir()
    for module in {c.module for c in CASES}:
        contents = []
        for case in CASES:
            if case.module != module:
                continue
            contents.append(
                "class LRUCache:\n    def __init__(self, *args):\n        raise NotImplementedError\n"
                if case.name == "LRUCache"
                else f"def {case.name}(*args, **kwargs):\n    raise NotImplementedError\n"
            )
        (exercises / f"{module}.py").write_text("\n".join(contents))
    return exercises


@pytest.mark.parametrize(
    "submission,expected", [("correct", "passed"), ("wrong", "failed"), ("todo", "not_implemented")]
)
def test_end_to_end_submission_report(tmp_path, submission, expected):
    exercises = isolated_checkout(tmp_path)
    code = (
        CORRECT_TWO_SUM
        if submission == "correct"
        else "def two_sum(nums, target):\n    "
        + ("return []\n" if submission == "wrong" else "raise NotImplementedError\n")
    )
    (exercises / "basic_structures.py").write_text(code)
    command = [
        sys.executable,
        "-c",
        "from phase1_python_programming.section01_data_structures.assessment.grader import main; raise SystemExit(main())",
        "--problem",
        "two_sum",
        "--output",
        str(tmp_path / "report"),
        "--time-multiplier",
        "10",
    ]
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, timeout=20)
    assert result.returncode == (0 if submission == "correct" else 1), result.stderr
    report = json.loads((tmp_path / "report/results.json").read_text())
    row = report["results"][0]
    assert row["correctness"]["status"] == expected
    assert row["correctness"]["total"] == 4
    for key in ["advanced_time", "advanced_memory"]:
        metric = row[key]
        if submission == "todo":
            assert metric["status"] == "not_implemented"
            assert metric["measured"] is metric["ratio"] is None
        else:
            assert metric["ratio"] == pytest.approx(metric["measured"] / metric["limit"])
            assert metric["status"] == ("passed" if submission == "correct" else "wrong_answer")
    assert report["all_passed"] == (submission == "correct")
    markdown = (tmp_path / "report/results.md").read_text()
    assert "Advanced Time Tests" in markdown and "Advanced Memory Tests" in markdown
    assert "required limit" in markdown


def test_all_correctness_items_are_mapped_without_running_solutions(tmp_path):
    isolated_checkout(tmp_path)
    results = tmp_path / "mapping.json"
    command = [
        sys.executable,
        "-m",
        "pytest",
        "phase1_python_programming/section01_data_structures/tests/test_basic_structures.py",
        "phase1_python_programming/section01_data_structures/tests/test_advanced_structures.py",
        "phase1_python_programming/section01_data_structures/tests/test_iterators_generators.py",
        "--collect-only",
        "-q",
        "-p",
        "phase1_python_programming.section01_data_structures.assessment.correctness_plugin",
        f"--section01-results={results}",
    ]
    process = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, timeout=15)
    assert process.returncode == 0, process.stderr
    data = json.loads(results.read_text())
    assert {item["problem"] for item in data["items"].values()} == {c.id for c in CASES}
    assert len(data["items"]) >= 90
