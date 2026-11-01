import dataclasses

import pytest

import phase1_python_programming.section02_python_engineering.exercises.oop_and_testing as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("values", [{}, {"a": 1}, {"a": 1, "b": 2}])
def test_record(values):
    r = m.DatasetRecord(3, values)
    assert dataclasses.is_dataclass(r)
    assert len(r) == len(values)
    assert r == m.DatasetRecord(3, values)
    assert "row_id=3" in repr(r)


@pytest.mark.parametrize("count", [0, 1, 3])
def test_collection(count):
    records = [object() for _ in range(count)]
    collection = m.DatasetCollection(iter(records))
    assert len(collection) == count
    assert list(collection) == records
    assert repr(collection) == f"DatasetCollection(rows={count})"
    item = object()
    collection.add(item)
    assert list(collection)[-1] is item
    assert len(collection) == count + 1
