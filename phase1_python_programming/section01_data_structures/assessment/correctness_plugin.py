"""Run existing correctness tests once and attribute every outcome to a problem."""

import json
from pathlib import Path

import pytest

from .cases import BY_NAME, CASES, select_cases


def pytest_addoption(parser):
    parser.addoption("--section01-results")
    parser.addoption("--section01-problems", default="")


def pytest_configure(config):
    config._section01_report = {"items": {}, "collection_errors": [], "finished": False}


def _write(config):
    path = Path(config.getoption("--section01-results"))
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(config._section01_report, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)


def pytest_collection_modifyitems(config, items):
    selected = (
        {case.id for case in select_cases(config.getoption("--section01-problems").split(","))}
        if config.getoption("--section01-problems")
        else {case.id for case in CASES}
    )
    kept, removed = [], []
    for item in items:
        name = item.originalname or item.name
        if name == "test_window_iterators_are_lazy":
            case = BY_NAME[item.callspec.params["name"]]
        else:
            matches = [case for case in CASES if name in case.tests]
            if len(matches) != 1:
                raise pytest.UsageError(
                    f"Correctness test has no unique Section 01 mapping: {item.nodeid}"
                )
            case = matches[0]
        if case.id in selected:
            kept.append(item)
            config._section01_report["items"][item.nodeid] = {"problem": case.id, "phases": {}}
            item._section01_config = config
        else:
            removed.append(item)
    items[:] = kept
    config.hook.pytest_deselected(items=removed)
    _write(config)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    config = item._section01_config
    entry = config._section01_report["items"][item.nodeid]
    status = "xfailed" if hasattr(report, "wasxfail") else report.outcome
    entry["phases"][report.when] = status
    if report.failed:
        entry["detail"] = str(report.longrepr)[-1600:]
    _write(config)


def pytest_collectreport(report):
    # Collection failures are captured from session at finish too; no item exists here.
    if report.failed:
        _COLLECTION_ERRORS.append(str(report.longrepr)[-1600:])


_COLLECTION_ERRORS = []


def pytest_sessionfinish(session, exitstatus):
    report = session.config._section01_report
    report["finished"] = True
    report["exit_code"] = int(exitstatus)
    report["collection_errors"] = list(_COLLECTION_ERRORS)
    _write(session.config)
