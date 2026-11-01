import numpy as np
import pandas as pd
import pytest

import phase2_data_science.section04_pandas.exercises.data_cleaning as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "values, count, ratio", [([1, None], 1, 0.5), ([], 0, 0.0), ([None, None], 2, 1.0)]
)
def test_missing(values, count, ratio):
    actual = m.missing_summary(pd.DataFrame({"a": values}))
    assert list(actual.columns) == ["missing_count", "missing_ratio"]
    assert actual.loc["a", "missing_count"] == count
    assert actual.loc["a", "missing_ratio"] == pytest.approx(ratio)


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"a": [1.0, np.nan, 3.0]}, {"a": [1.0, 2.0, 3.0]}),
        ({"a": [np.nan, np.nan]}, {"a": [0.0, 0.0]}),
        ({"s": ["x", None]}, {"s": ["x", "unknown"]}),
    ],
)
def test_fill(data, expected):
    before = pd.DataFrame(data)
    actual = m.fill_missing(before)
    pd.testing.assert_frame_equal(actual, pd.DataFrame(expected))
    pd.testing.assert_frame_equal(before, pd.DataFrame(data))


@pytest.mark.parametrize("values", [[1, 1, 2], [], [np.nan, np.nan, 1]])
def test_dedup(values):
    df = pd.DataFrame({"a": values})
    pd.testing.assert_frame_equal(m.remove_duplicates(df), df.drop_duplicates())


@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, 1, 1, 1, 100], [False, False, False, False, True]),
        ([], []),
        ([2, 2, np.nan], [False, False, False]),
    ],
)
def test_outliers(values, expected):
    df = pd.DataFrame({"x": values})
    pd.testing.assert_series_equal(
        m.detect_outliers(df, "x"), pd.Series(expected, name="x", dtype=bool)
    )
