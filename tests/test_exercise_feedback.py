"""The learning feedback must never disguise an incorrect implementation."""

from pathlib import Path

import pytest

pytest_plugins = ["pytester"]


@pytest.mark.parametrize(
    "body,arguments,expected",
    [
        ('    """TODO exercise."""\n    raise NotImplementedError\n', [], {"xfailed": 1}),
        ("    return 0\n", [], {"failed": 1}),
        ("    value = 1\n    raise NotImplementedError(value)\n", [], {"failed": 1}),
        ("    raise NotImplementedError\n", ["--strict-exercises"], {"failed": 1}),
    ],
    ids=["untouched", "wrong-answer", "implemented-exception", "strict"],
)
def test_feedback_policy(pytester, body, arguments, expected):
    root = Path(__file__).resolve().parents[1]
    pytester.makeconftest((root / "conftest.py").read_text(encoding="utf-8"))
    package = pytester.path / "exercises"
    package.mkdir()
    (package / "task.py").write_text("def solve():\n" + body, encoding="utf-8")
    pytester.makepyfile(
        test_solution="from exercises.task import solve\n\ndef test_answer():\n    assert solve() == 1\n"
    )
    result = pytester.runpytest_subprocess("-q", *arguments)
    result.assert_outcomes(**expected)
