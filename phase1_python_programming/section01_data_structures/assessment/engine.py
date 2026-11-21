"""Process isolation and result formatting shared by pytest and the submission grader."""

from __future__ import annotations

import ast
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from .cases import MIB, Case

ROOT = Path(__file__).resolve().parents[3]
WORKER_MODULE = "phase1_python_programming.section01_data_structures.assessment.worker"


def is_unimplemented(case: Case) -> bool:
    path = (
        ROOT / "phase1_python_programming/section01_data_structures/exercises" / f"{case.module}.py"
    )
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = next(
        n
        for n in tree.body
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == case.name
    )
    if isinstance(node, ast.ClassDef):
        node = next(n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == "__init__")
    body = node.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        body = body[1:]
    return (
        len(body) == 1
        and isinstance(body[0], ast.Raise)
        and isinstance(body[0].exc, (ast.Name, ast.Call))
        and (
            body[0].exc.id
            if isinstance(body[0].exc, ast.Name)
            else getattr(body[0].exc.func, "id", None)
        )
        == "NotImplementedError"
    )


def run_metric(
    case: Case,
    metric: str,
    *,
    time_multiplier: float = 1.0,
    repeats: int = 3,
    wall_timeout: float | None = None,
    target_module: str | None = None,
) -> dict:
    if metric not in {"time", "memory"}:
        raise ValueError("metric must be time or memory")
    if repeats < 1 or not math.isfinite(time_multiplier) or time_multiplier <= 0:
        raise ValueError("repeats and time multiplier must be positive")
    if wall_timeout is not None and (not math.isfinite(wall_timeout) or wall_timeout <= 0):
        raise ValueError("wall timeout must be finite and positive")
    limit = case.seconds * time_multiplier if metric == "time" else int(case.memory_mib * MIB)
    base = {
        "status": "not_implemented",
        "measured": None,
        "limit": limit,
        "ratio": None,
        "unit": "seconds" if metric == "time" else "bytes",
        "samples": [],
    }
    if target_module is None and is_unimplemented(case):
        return base
    with tempfile.TemporaryDirectory(prefix="section01-metric-") as temporary:
        result = Path(temporary) / "result.json"
        command = [
            sys.executable,
            "-m",
            WORKER_MODULE,
            "--problem",
            case.id,
            "--metric",
            metric,
            "--result",
            str(result),
            "--repeats",
            str(repeats),
            "--time-multiplier",
            str(time_multiplier),
        ]
        if target_module is not None:
            command.extend(["--target-module", target_module])
        environment = dict(os.environ, PYTHONHASHSEED="0")
        timeout = (
            wall_timeout
            if wall_timeout is not None
            else max(20.0, case.seconds * time_multiplier * repeats * 10 + 10)
        )
        try:
            process = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return dict(
                base,
                status="worker_timeout",
                detail=f"Worker exceeded {timeout:g}s wall-clock guard; no exact measurement available",
            )
        if not result.exists():
            return dict(
                base,
                status="worker_error",
                detail=f"Worker exited with code {process.returncode} without a result",
            )
        data = json.loads(result.read_text(encoding="utf-8"))
        return dict(base, **data)


def describe_metric(result: dict) -> str:
    if result["measured"] is None:
        return f"{result['status']} (not measured)"
    if result["unit"] == "seconds":
        values = f"{result['measured']:.6f}s / {result['limit']:.6f}s"
    else:
        values = f"{result['measured'] / MIB:.3f} MiB / {result['limit'] / MIB:.3f} MiB"
    return f"{values} = {result['ratio']:.2f}x ({result['status']})"
