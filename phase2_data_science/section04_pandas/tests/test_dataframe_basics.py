import pandas as pd
import pytest

import phase2_data_science.section04_pandas.exercises.dataframe_basics as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "content, expected",
    [
        ("a,b\n1,2\n", pd.DataFrame({"a": [1], "b": [2]})),
        ("a,b\n", pd.DataFrame(columns=["a", "b"])),
        ("a\n1\n2\n", pd.DataFrame({"a": [1, 2]})),
    ],
)
def test_load_dataset(tmp_path, content, expected):
    p = tmp_path / "data.csv"
    p.write_text(content)
    pd.testing.assert_frame_equal(m.load_dataset(p), expected)


@pytest.mark.parametrize("columns", [["b", "a"], [], ["a"]])
def test_select(columns):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]}, index=[8, 9])
    actual = m.select_columns(df, columns)
    pd.testing.assert_frame_equal(actual, df.loc[:, columns])
    if columns:
        actual.iloc[0, 0] = 99
        assert df.iloc[0, df.columns.get_loc(columns[0])] != 99


@pytest.mark.parametrize("mask", [[False, True], [False, False], [True, pd.NA]])
def test_filter(mask):
    df = pd.DataFrame({"a": [1, 2]}, index=[5, 6])
    condition = pd.Series(mask, index=df.index, dtype="boolean")
    pd.testing.assert_frame_equal(m.filter_rows(df, condition), df.loc[condition.fillna(False)])


@pytest.mark.parametrize("values", [[" A ", "B"], [], [" x ", None]])
def test_transform(values):
    df = pd.DataFrame({"name": pd.Series(values, dtype="object")})
    expected = df.copy()
    expected["name"] = expected["name"].map(
        lambda v: v.strip().lower() if isinstance(v, str) else v
    )
    before = df.copy(deep=True)
    pd.testing.assert_frame_equal(m.transform_column(df, "name"), expected)
    pd.testing.assert_frame_equal(df, before)


@pytest.mark.parametrize("values", [["2025-01-01", "bad"], [], [None, "2024-02-29"]])
def test_dates(values):
    df = pd.DataFrame({"date": values})
    actual = m.convert_dates(df, "date")
    expected = pd.Series(pd.to_datetime(values, errors="coerce").as_unit("ns"), name="date")
    pd.testing.assert_series_equal(actual["date"], expected)


@pytest.mark.parametrize("data", [{"a": [1, None], "b": [True, None]}, {}, {"s": ["a", None]}])
def test_dtypes(data):
    df = pd.DataFrame(data)
    pd.testing.assert_frame_equal(m.convert_dtypes(df), df.convert_dtypes())
