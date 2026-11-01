"""Reproducible datasets and deliberate corruption are part of the learning contract."""

import csv
import json

import numpy as np
import pytest

from scripts.generate_datasets import classification, generate


@pytest.mark.parametrize("seed", [1, 7, 42])
def test_core_datasets(tmp_path, seed):
    first, second = tmp_path / "first", tmp_path / "second"
    result = generate(first, seed, include_classification=False)
    generate(second, seed, include_classification=False)
    assert result["seed"] == seed
    assert json.loads((first / "manifest.json").read_text())["seed"] == seed
    for path in first.rglob("*"):
        if not path.is_file():
            continue
        other = second / path.relative_to(first)
        if path.suffix == ".npz":
            with np.load(path) as left, np.load(other) as right:
                for key in left.files:
                    np.testing.assert_array_equal(left[key], right[key])
        else:
            assert path.read_bytes() == other.read_bytes()
    for name, minimum in [("users", 1000), ("products", 100), ("orders", 10000)]:
        with (first / f"ecommerce/{name}.csv").open() as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) >= minimum
        assert len({json.dumps(row, sort_keys=True) for row in rows}) < len(rows)
        assert any("" in row.values() for row in rows)
    with (first / "ecommerce/products.csv").open() as handle:
        prices = [float(r["price"]) for r in csv.DictReader(handle) if r["price"]]
    assert min(prices) < 0 and max(prices) > 10000
    assert np.load(first / "vectors.npy").shape == (1000, 128)


@pytest.mark.parametrize("seed", [1, 7, 42])
def test_classification_generation(tmp_path, seed):
    classification(tmp_path, seed, size=80)
    with (tmp_path / "classification.csv").open() as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 80
    assert len(rows[0]) == 11
    assert {row["target"] for row in rows} == {"0", "1"}
