import hashlib

import pytest

import phase1_python_programming.section02_python_engineering.exercises.file_operations as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("names", [[], ["a.txt"], ["z.txt", "sub/b.txt", "a.txt"]])
def test_list_files(tmp_path, names):
    for name in names:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x")
    assert m.list_files(tmp_path) == sorted([tmp_path / n for n in names], key=str)


@pytest.mark.parametrize(
    "content, expected",
    [("a,b\n1,2\n", [{"a": "1", "b": "2"}]), ("", []), ('a,b\n"x,y",\n', [{"a": "x,y", "b": ""}])],
)
def test_read_csv(tmp_path, content, expected):
    p = tmp_path / "a.csv"
    p.write_text(content, encoding="utf-8")
    assert m.read_csv(p) == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        (({"b": " x ", "a": 1},), {"a": 1, "b": "x"}),
        (({},), {}),
        (([" y ", None, {"z": True}],), ["y", None, {"z": True}]),
    ],
)
def test_normalize_json(args, expected):
    result = m.normalize_json(*args)
    assert result == expected
    if isinstance(result, dict):
        assert list(result) == sorted(result)


@pytest.mark.parametrize("content", [b"", b"abc", b"xyz" * 100000])
def test_hash(tmp_path, content):
    p = tmp_path / "blob"
    p.write_bytes(content)
    assert m.calculate_file_hash(p) == hashlib.sha256(content).hexdigest()


@pytest.mark.parametrize(
    "contents, expected", [(["x", "x", "y"], [[0, 1]]), ([], []), (["", ""], [[0, 1]])]
)
def test_duplicates(tmp_path, contents, expected):
    paths = []
    for i, content in enumerate(contents):
        p = tmp_path / str(i)
        p.write_text(content)
        paths.append(p)
    assert m.find_duplicates(tmp_path) == [[paths[i] for i in group] for group in expected]


@pytest.mark.parametrize("mapping,dry_run", [({"a": "b"}, True), ({"a": "b"}, False), ({}, True)])
def test_rename(tmp_path, mapping, dry_run):
    (tmp_path / "a").write_text("x")
    expected = [(tmp_path / "a", tmp_path / "b")] if mapping else []
    assert m.batch_rename(tmp_path, mapping, dry_run) == expected
    applied = bool(mapping) and not dry_run
    assert (tmp_path / "a").exists() != applied
    assert (tmp_path / "b").exists() == applied


@pytest.mark.parametrize("mapping", [{"a": "../out"}, {"a": "b", "b": "a"}, {"a": "c", "b": "c"}])
def test_rename_invalid(tmp_path, mapping):
    for name in ["a", "b"]:
        (tmp_path / name).write_text(name)
    with pytest.raises((ValueError, FileExistsError)):
        m.batch_rename(tmp_path, mapping, False)
    assert (tmp_path / "a").read_text() == "a"
    assert (tmp_path / "b").read_text() == "b"
