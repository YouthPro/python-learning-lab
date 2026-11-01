import matplotlib.pyplot as plt
import numpy as np
import pytest

import phase2_data_science.section05_matplotlib.exercises.basic_plots as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("x,y", [([0, 1], [2, 3]), ([], []), ([1], [5])])
def test_plot_line(x, y):
    fig, ax = m.plot_line(x, y)
    try:
        np.testing.assert_allclose(ax.lines[0].get_xdata(), x)
        np.testing.assert_allclose(ax.lines[0].get_ydata(), y)
        assert ax.get_title() and ax.get_xlabel() and ax.get_ylabel()
        assert ax.get_legend() is not None
    finally:
        plt.close(fig)


@pytest.mark.parametrize("labels,values", [(["A", "B"], [1, 2]), ([], []), (["A"], [0])])
def test_plot_bar(labels, values):
    fig, ax = m.plot_bar(labels, values)
    try:
        np.testing.assert_allclose([p.get_height() for p in ax.patches], values)
        assert ax.get_title() and ax.get_xlabel() and ax.get_ylabel()
    finally:
        plt.close(fig)


@pytest.mark.parametrize("data", [[1, 1, 2], [], [5]])
def test_plot_hist(data):
    fig, ax = m.plot_hist(data)
    try:
        assert sum(p.get_height() for p in ax.patches) == len(data)
        assert len(ax.patches) == 10
        assert ax.get_title() and ax.get_xlabel() and ax.get_ylabel()
    finally:
        plt.close(fig)


@pytest.mark.parametrize("x,y", [([1, 2], [3, 4]), ([], []), ([1], [0])])
def test_plot_scatter(x, y):
    fig, ax = m.plot_scatter(x, y)
    try:
        np.testing.assert_allclose(
            ax.collections[0].get_offsets(), np.array(list(zip(x, y))).reshape(-1, 2)
        )
        assert ax.get_title() and ax.get_xlabel() and ax.get_ylabel()
    finally:
        plt.close(fig)


@pytest.mark.parametrize("data", [[[1, 2], [3, 4]], [], [[5]]])
def test_plot_box(data):
    fig, ax = m.plot_box(data)
    try:
        assert len(ax.patches) == len(data)
        assert ax.get_title() and ax.get_xlabel() and ax.get_ylabel()
    finally:
        plt.close(fig)
