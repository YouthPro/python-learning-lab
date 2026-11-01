import json

import numpy as np
import pandas as pd
import pytest

from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.analysis import analyze
from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.cleaning import (
    clean_tables,
    table_quality,
)
from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.data_loader import (
    load_tables,
)
from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.reporting import (
    save_reports,
)


@pytest.mark.parametrize("quantity", [1, 2, 5])
def test_known_sales(tmp_path, quantity):
    raw = {
        "users": pd.DataFrame(
            {
                "user_id": [1, 2],
                "age": [20, np.nan],
                "gender": ["F", "M"],
                "city": ["X", None],
                "register_date": ["2023-01-01", "2023-02-01"],
            }
        ),
        "products": pd.DataFrame(
            {
                "product_id": [1, 2],
                "product_name": ["P", "Q"],
                "category": ["A", "A"],
                "price": [10.0, -1.0],
            }
        ),
        "orders": pd.DataFrame(
            {
                "order_id": [1, 1, 2, 3],
                "user_id": [1, 1, 1, 2],
                "product_id": [1, 1, 2, 1],
                "quantity": [quantity, quantity, 2, -1],
                "order_date": ["2024-01-01"] * 4,
            }
        ),
    }
    for name, frame in raw.items():
        frame.to_csv(tmp_path / f"{name}.csv", index=False)
    loaded = load_tables(tmp_path)
    before = {k: v.copy(deep=True) for k, v in loaded.items()}
    clean, quality = clean_tables(loaded)
    result = analyze(clean)
    assert result["summary"]["total_sales"] == 10 * quantity + 20
    assert result["summary"]["average_spend_per_user"] == (10 * quantity + 20) / 2
    assert result["summary"]["order_count"] == 2
    assert quality["before"]["orders"]["duplicates"] == 1
    assert table_quality(clean["orders"])["duplicates"] == 0
    assert result["sales_analysis"]["sales"].sum() == result["category_analysis"]["sales"].sum()
    assert result["registration_cohorts"]["buyers"].sum() == 1
    for name in before:
        pd.testing.assert_frame_equal(before[name], loaded[name])
    save_reports(clean, result, quality, tmp_path / "reports")
    assert json.loads((tmp_path / "reports/summary.json").read_text()) == result["summary"]
    for file in [
        "data_quality_report.md",
        "sales_analysis.csv",
        "customer_analysis.csv",
        "product_analysis.csv",
    ]:
        assert (tmp_path / "reports" / file).exists()


@pytest.mark.parametrize(
    "columns", [["user_id", "age"], ["product_id", "price"], ["order_id", "quantity", "order_date"]]
)
def test_empty_quality(columns):
    assert table_quality(pd.DataFrame(columns=columns)) == {
        "rows": 0,
        "columns": len(columns),
        "duplicates": 0,
        "missing": {column: {"count": 0, "ratio": 0.0} for column in columns},
    }
