import hashlib
import json

import pytest

from phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit import (
    operations as m,
)


@pytest.mark.parametrize("values", [[], ["x"], ["x", "x", "y"]])
def test_scan_and_duplicates(tmp_path, values):
    for i, value in enumerate(values):
        (tmp_path / str(i)).write_text(value)
    files = m.list_files(tmp_path)
    assert len(files) == len(values)
    for p in files:
        assert m.calculate_file_hash(p) == hashlib.sha256(p.read_bytes()).hexdigest()
    groups = m.find_duplicates(tmp_path)
    assert len(groups) == (1 if len(values) == 3 else 0)


@pytest.mark.parametrize("mapping,apply", [({"a": "b"}, False), ({"a": "b"}, True), ({}, False)])
def test_rename(tmp_path, mapping, apply):
    (tmp_path / "a").write_text("data")
    plan = m.batch_rename(tmp_path, mapping, dry_run=not apply)
    assert plan == ([(tmp_path / "a", tmp_path / "b")] if mapping else [])
    assert (tmp_path / "b").exists() == apply


@pytest.mark.parametrize("mapping", [{"a": "../out"}, {"a": "b", "b": "a"}, {"a": "c", "b": "c"}])
def test_rename_preflight(tmp_path, mapping):
    for name in ["a", "b"]:
        (tmp_path / name).write_text(name)
    with pytest.raises((ValueError, FileExistsError)):
        m.batch_rename(tmp_path, mapping, False)
    assert (tmp_path / "a").read_text() == "a"
    assert (tmp_path / "b").read_text() == "b"


@pytest.mark.parametrize("rows", [[], ["1,2"], ["1,2", "3,4"]])
def test_merge(tmp_path, rows):
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    for p in [a, b]:
        p.write_text("x,y\n" + "\n".join(rows))
    out = tmp_path / "merged.csv"
    assert m.merge_csv([a, b], out) == len(rows) * 2
    assert not out.exists()
    assert m.merge_csv([a, b], out, False) == len(rows) * 2
    assert len(out.read_text().splitlines()) == len(rows) * 2 + 1
    with pytest.raises(FileExistsError):
        m.merge_csv([a], out, False)


@pytest.mark.parametrize("data", [{"b": " x ", "a": 1}, [], [{"x": " hi "}]])
def test_normalize(tmp_path, data):
    source, out = tmp_path / "in.json", tmp_path / "out.json"
    source.write_text(json.dumps(data))
    expected = m.normalize_json(data)
    assert m.normalize_file(source, out) == expected
    assert not out.exists()
    assert m.normalize_file(source, out, False) == expected
    assert json.loads(out.read_text()) == expected


def test_header_mismatch(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_text("a\n1")
    b.write_text("b\n2")
    with pytest.raises(ValueError):
        m.merge_csv([a, b], tmp_path / "out", False)
    assert not (tmp_path / "out").exists()
