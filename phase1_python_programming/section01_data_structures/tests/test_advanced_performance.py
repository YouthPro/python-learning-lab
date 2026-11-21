"""Opt-in stress tests; each metric is measured in a fresh subprocess."""

import pytest

from phase1_python_programming.section01_data_structures.assessment.cases import CASES
from phase1_python_programming.section01_data_structures.assessment.engine import (
    describe_metric,
    run_metric,
)

pytestmark = pytest.mark.exercise


def _check(case, metric, request, record_property):
    result = run_metric(
        case, metric, time_multiplier=request.config.getoption("--advanced-time-multiplier")
    )
    if result["status"] == "not_implemented":
        if request.config.getoption("--strict-exercises"):
            pytest.fail(f"{case.name}: TODO is not implemented")
        pytest.xfail("Untouched exercise TODO; no performance measurement available")
    record_property("problem", case.name)
    record_property("measurement", result["measured"])
    record_property("required", result["limit"])
    record_property("ratio", result["ratio"])
    assert result["status"] == "passed", (
        f"{case.name}: {describe_metric(result)}; {result.get('detail', '')}"
    )


@pytest.mark.advanced_time
@pytest.mark.parametrize("case", CASES, ids=lambda c: f"Advanced Time Tests-{c.id}-{c.name}")
def test_advanced_time(case, request, record_property):
    _check(case, "time", request, record_property)


@pytest.mark.advanced_memory
@pytest.mark.parametrize("case", CASES, ids=lambda c: f"Advanced Memory Tests-{c.id}-{c.name}")
def test_advanced_memory(case, request, record_property):
    _check(case, "memory", request, record_property)
