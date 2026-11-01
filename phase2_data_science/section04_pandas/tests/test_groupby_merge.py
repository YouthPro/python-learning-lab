import numpy as np
import pandas as pd
import pytest

import phase2_data_science.section04_pandas.exercises.groupby_merge as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "data",
    [
        {"category": ["B", "A", "A"], "amount": [2.0, 1.0, 3.0]},
        {"category": pd.Series([], dtype=str), "amount": pd.Series([], dtype=float)},
        {"category": ["A", "A"], "amount": [np.nan, 2.0]},
    ],
)
def test_group_statistics(data):
    df = pd.DataFrame(data)
    expected = df.groupby("category")["amount"].agg(["sum", "mean", "count"])
    pd.testing.assert_frame_equal(m.group_statistics(df), expected)


@pytest.mark.parametrize(
    "categories, amounts", [(["A", "A", "B"], [1.0, 3.0, 8.0]), ([], []), (["A", None], [2.0, 5.0])]
)
def test_group_transform(categories, amounts):
    df = pd.DataFrame({"category": categories, "amount": amounts})
    expected = df.copy()
    expected["category_mean"] = df.groupby("category")["amount"].transform("mean")
    pd.testing.assert_frame_equal(m.group_transform(df), expected)


@pytest.mark.parametrize("ids", [[1, 2], [], [1, 1, 9]])
def test_merge(ids):
    left = pd.DataFrame({"user_id": pd.Series(ids, dtype="int64"), "v": range(len(ids))})
    right = pd.DataFrame({"user_id": [1, 2], "city": ["X", "Y"]})
    pd.testing.assert_frame_equal(
        m.merge_tables(left, right),
        left.merge(right, on="user_id", how="left", validate="many_to_one"),
    )


def test_merge_invalid():
    df = pd.DataFrame({"user_id": [1, 1]})
    with pytest.raises(pd.errors.MergeError):
        m.merge_tables(df, df)


@pytest.mark.parametrize(
    "rows",
    [[("X", "A", 2.0), ("X", "B", 3.0), ("Y", "A", 1.0)], [], [("X", "A", 1.0), ("X", "A", 2.0)]],
)
def test_pivot(rows):
    df = pd.DataFrame(rows, columns=["city", "category", "amount"]).astype({"amount": float})
    expected = df.pivot_table(
        index="city",
        columns="category",
        values="amount",
        aggfunc="sum",
        fill_value=0,
        observed=True,
    )
    pd.testing.assert_frame_equal(m.create_pivot(df), expected)


@pytest.mark.parametrize("values, window", [([1.0, 3.0, 5.0], 2), ([], 3), ([np.nan, 2.0, 4.0], 1)])
def test_rolling(values, window):
    df = pd.DataFrame({"amount": pd.Series(values, dtype=float)})
    expected = df.assign(rolling_mean=df["amount"].rolling(window, min_periods=1).mean())
    pd.testing.assert_frame_equal(m.rolling_average(df, window), expected)


def test_rolling_invalid():
    with pytest.raises(ValueError):
        m.rolling_average(pd.DataFrame({"amount": [1]}), 0)
