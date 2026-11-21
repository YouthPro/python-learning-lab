"""One workload/metric per process; timing and allocation tracing never overlap."""

from __future__ import annotations

import argparse
import gc
import importlib
import json
import math
import signal
import statistics
import tempfile
import time
import tracemalloc
from pathlib import Path

from .cases import BY_ID, MIB
from .workloads import make_workload


class MeasurementDeadline(Exception):
    """An operation exceeded the execution guard, independently of its pass budget."""


def _alarm(signum, frame):
    raise MeasurementDeadline("Operation exceeded execution guard")


def _memory_guard():
    # Guard the test host against accidental quadratic allocations. This is not the
    # graded memory measurement: that is tracemalloc's incremental allocation peak.
    try:
        import resource
    except ImportError:
        return False
    if not hasattr(resource, "RLIMIT_AS"):
        return False
    _, hard = resource.getrlimit(resource.RLIMIT_AS)
    ceiling = 512 * MIB if hard == resource.RLIM_INFINITY else min(512 * MIB, hard)
    resource.setrlimit(resource.RLIMIT_AS, (ceiling, hard))
    return True


def measure(
    case, target, metric: str, directory: Path, repeats: int = 3, time_multiplier: float = 1.0
) -> dict:
    if metric not in {"time", "memory"}:
        raise ValueError("metric must be time or memory")
    if repeats < 1 or not math.isfinite(time_multiplier) or time_multiplier <= 0:
        raise ValueError("repeats and time multiplier must be positive")
    samples = []
    limit = case.seconds * time_multiplier if metric == "time" else int(case.memory_mib * MIB)
    status, detail = "passed", ""
    for index in range(repeats if metric == "time" else 1):
        clear = getattr(target, "cache_clear", None)
        if clear is not None:
            clear()
        workload = make_workload(case.name, target, directory / str(index))
        gc.collect()
        started = None
        output = None
        # Signal guards interrupt Python loops on Unix. Parent watchdog also covers
        # preparation/imports and platforms without SIGALRM.
        alarms = hasattr(signal, "setitimer") and hasattr(signal, "SIGALRM")
        try:
            if alarms:
                signal.signal(signal.SIGALRM, _alarm)
                signal.setitimer(
                    signal.ITIMER_REAL,
                    max(1.0, case.seconds * time_multiplier * 8) if metric == "time" else 10.0,
                )
            if metric == "memory":
                tracemalloc.start()
                tracemalloc.reset_peak()
            else:
                started = time.perf_counter()
            output = workload.operation()
            value = (
                time.perf_counter() - started
                if metric == "time"
                else tracemalloc.get_traced_memory()[1]
            )
            samples.append(value)
        except MeasurementDeadline as exc:
            status, detail = "timeout", str(exc)
            if started is not None:
                samples.append(time.perf_counter() - started)
        except MemoryError:
            status, detail = "memory_guard", "Worker reached its process allocation guard"
        except Exception as exc:
            status, detail = "error", f"{type(exc).__name__}: {str(exc)[:1000]}"
        finally:
            if alarms:
                signal.setitimer(signal.ITIMER_REAL, 0)
            if metric == "memory" and tracemalloc.is_tracing():
                if status != "passed":
                    samples.append(tracemalloc.get_traced_memory()[1])
                tracemalloc.stop()
        if status != "passed":
            break
        # Excluded from the metrics. Keep the output alive until after peak readout.
        try:
            workload.validate(output)
        except Exception as exc:
            status, detail = "wrong_answer", f"{type(exc).__name__}: {str(exc)[:1000]}"
            break
        del output, workload
    measured = statistics.median(samples) if samples else None
    # A timed-out partial sample is diagnostic, never a passing median of earlier runs.
    if status == "timeout" and samples:
        measured = samples[-1]
    if status == "passed" and measured > limit:
        status = "failed_limit"
    return {
        "status": status,
        "measured": measured,
        "limit": limit,
        "ratio": measured / limit if measured is not None else None,
        "unit": "seconds" if metric == "time" else "bytes",
        "samples": samples,
        "detail": detail,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problem", required=True, choices=BY_ID)
    parser.add_argument("--metric", required=True, choices=["time", "memory"])
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--time-multiplier", type=float, default=1.0)
    parser.add_argument("--target-module")
    args = parser.parse_args()
    guard = _memory_guard()
    case = BY_ID[args.problem]
    try:
        module = importlib.import_module(args.target_module or case.target_module)
        target = getattr(module, case.name)
        with tempfile.TemporaryDirectory(prefix="section01-inputs-") as temporary:
            result = measure(
                case, target, args.metric, Path(temporary), args.repeats, args.time_multiplier
            )
    except Exception as exc:
        result = {
            "status": "error",
            "measured": None,
            "ratio": None,
            "samples": [],
            "detail": f"{type(exc).__name__}: {str(exc)[:1000]}",
        }
    result["process_address_space_guard"] = guard
    args.result.write_text(json.dumps(result, allow_nan=False), encoding="utf-8")


if __name__ == "__main__":
    main()
