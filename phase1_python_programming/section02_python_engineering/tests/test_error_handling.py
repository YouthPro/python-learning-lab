import json
import logging

import pytest

import phase1_python_programming.section02_python_engineering.exercises.error_handling as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("content", ['{"a":1}', "[]", "null"])
def test_json_success(tmp_path, caplog, content):
    p = tmp_path / "data.json"
    p.write_text(content)
    assert m.load_json_safely(p, logging.getLogger("exercise")) == json.loads(content)
    assert not [r for r in caplog.records if r.levelno >= logging.ERROR]


@pytest.mark.parametrize("kind", ["missing", "empty", "invalid"])
def test_json_errors(tmp_path, caplog, kind):
    p = tmp_path / "data.json"
    if kind != "missing":
        p.write_text("" if kind == "empty" else "{bad")
    with pytest.raises(m.DatasetError) as exc:
        m.load_json_safely(p, logging.getLogger("exercise"))
    assert exc.value.__cause__ is not None
    assert any(r.levelno == logging.ERROR for r in caplog.records)
