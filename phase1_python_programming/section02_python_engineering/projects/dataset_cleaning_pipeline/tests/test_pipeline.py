import csv

import pytest

from phase1_python_programming.section02_python_engineering.projects.dataset_cleaning_pipeline.src.cleaning_pipeline import (
    CleaningPipeline,
    clean_file,
    convert_types,
    deduplicate,
    fill_missing,
    select_columns,
)


@pytest.mark.parametrize(
    "rows", [[], [{"a": "1", "b": None}], [{"a": "2", "b": "x"}, {"a": "2", "b": "x"}]]
)
def test_steps(rows):
    before = [dict(r) for r in rows]
    steps = [
        lambda r: fill_missing(r, {"b": "unknown"}),
        deduplicate,
        lambda r: convert_types(r, {"a": int}),
        lambda r: select_columns(r, ["a"]),
    ]
    result = CleaningPipeline(steps).run(rows)
    assert rows == before
    assert result == ([{"a": int(rows[0]["a"])}] if rows else [])


@pytest.mark.parametrize("rows", [[], ["1,X"], ["1,X", "1,X", "2,"]])
def test_file(tmp_path, rows):
    source, out = tmp_path / "in.csv", tmp_path / "out.csv"
    source.write_text("a,b\n" + "\n".join(rows))
    pipe = CleaningPipeline([lambda r: fill_missing(r, {"b": "unknown"}), deduplicate])
    report = clean_file(source, out, pipe)
    assert report["before"]["rows"] == len(rows)
    assert report["after"]["rows"] == len(set(rows))
    with out.open() as handle:
        assert len(list(csv.DictReader(handle))) == len(set(rows))
    with pytest.raises(FileExistsError):
        clean_file(source, out, pipe)
