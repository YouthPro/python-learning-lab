import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import phase2_data_science.section05_matplotlib.exercises.advanced_plots as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "df", [pd.DataFrame(), pd.DataFrame({"a": ["x"]}), pd.DataFrame({"a": ["x"], "b": ["y"]})]
)
def test_correlation_requires_numeric_columns(df):
    with pytest.raises(ValueError):
        m.plot_correlation(df)


@pytest.mark.parametrize(
    "data", [{"a": [1, 2, 3], "b": [3, 2, 1]}, {"x": [1, 2, 3]}, {"a": [1, 1], "b": [2, 2]}]
)
def test_correlation(data):
    df = pd.DataFrame(data)
    fig, ax = m.plot_correlation(df)
    try:
        np.testing.assert_allclose(ax.images[0].get_array(), df.corr(), equal_nan=True)
        assert ax.images[0].get_clim() == (-1, 1)
        assert len(fig.axes) == 2
        assert ax.get_title() and ax.get_xlabel() and ax.get_ylabel()
    finally:
        plt.close(fig)


@pytest.mark.parametrize("values", [[1, 2, 3], [], [1]])
def test_dashboard(values):
    fig, axes = m.plot_dashboard({"x": list(range(len(values))), "y": values, "values": values})
    try:
        assert axes.shape == (2, 2)
        assert len(fig.axes) == 4
        assert all(ax.get_title() and ax.get_xlabel() and ax.get_ylabel() for ax in axes.flat)
    finally:
        plt.close(fig)


@pytest.mark.parametrize("name", ["a.png", "sub/b.png", "deep/sub/c.png"])
def test_save(tmp_path, name):
    fig, ax = plt.subplots()
    try:
        ax.plot([1, 2])
        path = tmp_path / name
        assert m.save_figure(fig, path) == path
        assert path.read_bytes().startswith(b"\x89PNG")
        assert plt.fignum_exists(fig.number)
    finally:
        plt.close(fig)
