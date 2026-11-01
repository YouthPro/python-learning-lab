import json

import pytest

from phase1_python_programming.section02_python_engineering.projects.dataset_inspector.src.dataset_inspector.manager import (
    DatasetManager,
    is_missing,
    numeric,
)
from phase1_python_programming.section02_python_engineering.projects.dataset_inspector.src.dataset_inspector.reporter import (
    save_report,
    to_markdown,
)


@pytest.mark.parametrize("suffix", ["csv", "json", "CSV"])
def test_load_and_summary(tmp_path, suffix):
    path = tmp_path / f"data.{suffix}"
    rows = [{"age": 20, "city": "X"}, {"age": None, "city": "Y"}, {"age": 20, "city": "X"}]
    path.write_text(json.dumps(rows) if suffix == "json" else "age,city\n20,X\n,Y\n20,X\n")
    manager = DatasetManager.from_file(path)
    report = manager.summary()
    assert (report["rows"], report["columns"], report["duplicate_rows"]) == (3, 2, 1)
    assert report["missing_values"]["age"] == {"count": 1, "ratio": 1 / 3}
    assert report["column_statistics"]["age"]["mean"] == 20
    assert report["column_statistics"]["city"]["unique_values"] == 2
    assert "# Dataset Summary" in to_markdown(report)
    save_report(report, tmp_path / "reports")
    assert json.loads((tmp_path / "reports/summary.json").read_text()) == json.loads(
        json.dumps(report)
    )


@pytest.mark.parametrize("strategy,n,missing", [("keep", 2, 1), ("drop", 1, 0), ("fill", 2, 0)])
def test_clean(strategy, n, missing):
    manager = DatasetManager([{"a": 1}, {"a": None}])
    result = manager.clean(strategy).summary()
    assert result["rows"] == n
    assert result["missing_values"]["a"]["count"] == missing
    assert manager.summary()["rows"] == 2


@pytest.mark.parametrize("rows,columns", [([], []), ([], ["a"]), ([{"a": None}], ["a"])])
def test_empty(rows, columns):
    report = DatasetManager(rows, columns).summary()
    json.dumps(report, allow_nan=False)
    assert report["columns"] == len(columns)


@pytest.mark.parametrize(
    "value,missing,number", [(None, True, None), ("", True, None), ("3", False, 3.0)]
)
def test_helpers(value, missing, number):
    assert is_missing(value) == missing
    assert numeric(value) == number


@pytest.mark.parametrize("text", ["{}", "[1]", "bad"])
def test_invalid(tmp_path, text):
    path = tmp_path / "bad.json"
    path.write_text(text)
    with pytest.raises(ValueError):
        DatasetManager.from_file(path)
