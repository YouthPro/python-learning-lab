"""Performance checks are opt-in so routine correctness feedback remains fast."""

import pytest


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-advanced"):
        return
    for item in items:
        if item.get_closest_marker("advanced_time") or item.get_closest_marker("advanced_memory"):
            item.add_marker(
                pytest.mark.skip(reason="Advanced performance tests: enable with --run-advanced")
            )
