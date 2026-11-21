"""Correctness + Advanced Time Tests + Advanced Memory Tests, with JSON/Markdown output."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from .cases import SECTION, Case, select_cases
from .engine import ROOT, describe_metric, is_unimplemented, run_metric

CORRECTNESS_FILES = [
    f"phase1_python_programming/section01_data_structures/tests/test_{name}.py"
    for name in ["basic_structures", "advanced_structures", "iterators_generators"]
]


def run_correctness(cases: list[Case], timeout: float = 30.0) -> dict:
    with tempfile.TemporaryDirectory(prefix="section01-correctness-") as temporary:
        path = Path(temporary) / "correctness.json"
        command = [
            sys.executable,
            "-m",
            "pytest",
            *CORRECTNESS_FILES,
            "--strict-exercises",
            "-q",
            "-p",
            f"{SECTION}.assessment.correctness_plugin",
            f"--section01-results={path}",
            f"--section01-problems={','.join(c.id for c in cases)}",
        ]
        state = "finished"
        environment = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONHASHSEED="0")
        try:
            process = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout,
            )
            exit_code = process.returncode
        except subprocess.TimeoutExpired:
            state, exit_code = "timeout", None
        data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    results = {}
    for case in cases:
        items = [value for value in data.get("items", {}).values() if value["problem"] == case.id]
        passed = failed = skipped = incomplete = 0
        failures = []
        for entry in items:
            phases = entry["phases"]
            if "failed" in phases.values():
                failed += 1
                failures.append(entry.get("detail", "Test setup or teardown failed"))
            elif "skipped" in phases.values() or "xfailed" in phases.values():
                skipped += 1
            elif all(phases.get(phase) == "passed" for phase in ["setup", "call", "teardown"]):
                passed += 1
            else:
                incomplete += 1
        status = (
            "failed" if failed else "incomplete" if incomplete or skipped or not items else "passed"
        )
        try:
            if is_unimplemented(case):
                status = "not_implemented"
                failures = []
        except (SyntaxError, OSError, StopIteration):
            status = "source_error"
        results[case.id] = {
            "status": status,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "incomplete": incomplete,
            "total": len(items),
            "failures": failures,
        }
    return {
        "state": state,
        "exit_code": exit_code,
        "finished": data.get("finished", False),
        "collection_errors": data.get("collection_errors", []),
        "problems": results,
    }


def assess(
    cases: list[Case],
    *,
    time_multiplier: float = 1.0,
    repeats: int = 3,
    correctness_timeout: float = 30.0,
) -> dict:
    correctness = run_correctness(cases, correctness_timeout)
    rows = []
    for case in cases:
        metrics = {}
        for metric in ["time", "memory"]:
            try:
                metrics[metric] = run_metric(
                    case, metric, time_multiplier=time_multiplier, repeats=repeats
                )
            except (SyntaxError, OSError, StopIteration) as exc:
                metrics[metric] = {
                    "status": "source_error",
                    "measured": None,
                    "limit": case.seconds * time_multiplier
                    if metric == "time"
                    else int(case.memory_mib * 1024 * 1024),
                    "ratio": None,
                    "unit": "seconds" if metric == "time" else "bytes",
                    "samples": [],
                    "detail": f"{type(exc).__name__}: {exc}",
                }
        row = {
            "id": case.id,
            "name": case.name,
            "correctness": correctness["problems"][case.id],
            "advanced_time": metrics["time"],
            "advanced_memory": metrics["memory"],
        }
        row["passed"] = all(
            row[key]["status"] == "passed"
            for key in ["correctness", "advanced_time", "advanced_memory"]
        )
        rows.append(row)
    modules = {case.module for case in cases}
    hashes = {}
    for module in sorted(modules):
        path = ROOT / f"phase1_python_programming/section01_data_structures/exercises/{module}.py"
        hashes[module] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": sys.version,
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "perf_counter_resolution_seconds": time.get_clock_info("perf_counter").resolution,
        },
        "settings": {
            "time_multiplier": time_multiplier,
            "time_repeats": repeats,
            "memory_repeats": 1,
            "memory_measure": "peak incremental Python allocations via tracemalloc; input/expected excluded, output included",
            "correctness_timeout_seconds": correctness_timeout,
        },
        "source_sha256": hashes,
        "correctness_run": {k: v for k, v in correctness.items() if k != "problems"},
        "results": rows,
        "all_passed": all(row["passed"] for row in rows) and correctness["exit_code"] == 0,
    }


def render_markdown(report: dict, *, include_details: bool = True) -> str:
    lines = [
        "# Section 01 Submission Results",
        "",
        "Ratios are **your measured usage / required limit**; ≤ 1.00× meets the limit. A problem passes only when correctness and both advanced tests pass.",
        "",
        "| Problem | Correctness | Advanced Time Tests | Advanced Memory Tests | Overall |",
        "|---|---|---|---|---|",
    ]
    for row in report["results"]:
        correct = row["correctness"]
        lines.append(
            f"| {row['id']} {row['name']} | {correct['status']} ({correct['passed']}/{correct['total']}) | {describe_metric(row['advanced_time'])} | {describe_metric(row['advanced_memory'])} | {'PASS' if row['passed'] else 'NOT PASSED'} |"
        )
    lines.extend(
        [
            "",
            "Memory is Python allocation peak, **not whole-process RSS**. Time excludes input preparation, interpreter startup and output validation; generator consumption is included. Performance results do not override correctness failures.",
            "",
            f"Correctness runner: {report['correctness_run']['state']} (exit={report['correctness_run']['exit_code']}). Time multiplier: {report['settings']['time_multiplier']}; median of {report['settings']['time_repeats']} time runs.",
            "",
            f"Environment: {report['environment']['implementation']} {report['environment']['platform']}",
            "",
            f"Created: {report['created_at']}",
        ]
    )
    errors = report["correctness_run"]["collection_errors"]
    for row in report["results"]:
        failures = row["correctness"]["failures"]
        details = [row[key].get("detail", "") for key in ["advanced_time", "advanced_memory"]]
        if include_details and (failures or any(details)):
            lines.extend(
                [
                    "",
                    f"## {row['id']} {row['name']} details",
                    "",
                    "```text",
                    "\n".join([*failures, *filter(None, details)]),
                    "```",
                ]
            )
    if errors:
        lines.extend(
            ["", "## Correctness collection errors", "", "```text", "\n".join(errors), "```"]
        )
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--problem", nargs="+", help="Problem IDs or function/class names; default: all 30"
    )
    parser.add_argument(
        "--output", type=Path, default=ROOT / "datasets/processed/section01_assessment"
    )
    parser.add_argument(
        "--time-multiplier",
        type=float,
        default=1.0,
        help="Explicit hardware adjustment (recorded in report); memory limits stay fixed",
    )
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--correctness-timeout", type=float, default=30.0)
    args = parser.parse_args(argv)
    if args.repeats < 1 or not all(
        math.isfinite(v) and v > 0 for v in [args.time_multiplier, args.correctness_timeout]
    ):
        parser.error("repeats, time multiplier and correctness timeout must be finite and positive")
    try:
        cases = select_cases(args.problem)
    except ValueError as exc:
        parser.error(str(exc))
    report = assess(
        cases,
        time_multiplier=args.time_multiplier,
        repeats=args.repeats,
        correctness_timeout=args.correctness_timeout,
    )
    args.output.mkdir(parents=True, exist_ok=True)
    json_path, markdown_path = args.output / "results.json", args.output / "results.md"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
    )
    markdown = render_markdown(report)
    markdown_path.write_text(markdown, encoding="utf-8")
    print(render_markdown(report, include_details=False))
    print(f"JSON: {json_path}\nMarkdown: {markdown_path}")
    return 0 if report["all_passed"] else 1
