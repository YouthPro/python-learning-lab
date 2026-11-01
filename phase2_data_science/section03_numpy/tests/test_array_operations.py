import numpy as np
import pytest

import phase2_data_science.section03_numpy.exercises.array_operations as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "args, expected",
    [
        (([1, 2],), np.array([1.0, 2.0])),
        (([],), np.array([])),
        (([[1, 2], [3, 4]],), np.array([[1.0, 2.0], [3.0, 4.0]])),
    ],
)
def test_create_array(args, expected):
    result = m.create_array(*args)
    assert result.dtype == np.float64
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.arange(6), (2, 3)), np.arange(6).reshape(2, 3)),
        ((np.array([]), (0, 2)), np.empty((0, 2))),
        ((np.arange(4), (-1, 2)), np.array([[0, 1], [2, 3]])),
    ],
)
def test_transform_shape(args, expected):
    result = m.transform_shape(*args)
    np.testing.assert_allclose(result, expected)


def test_shape_invalid():
    with pytest.raises(ValueError):
        m.transform_shape(np.arange(3), (2, 2))


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.arange(9).reshape(3, 3), slice(1, 3), slice(0, 2)), np.array([[3, 4], [6, 7]])),
        ((np.empty((0, 2)), slice(None), slice(None)), np.empty((0, 2))),
        (
            (np.arange(4).reshape(2, 2), slice(None, None, -1), slice(None)),
            np.array([[2, 3], [0, 1]]),
        ),
    ],
)
def test_slice_matrix(args, expected):
    result = m.slice_matrix(*args)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([1, 2]), np.array([True, False])), np.array([1])),
        ((np.array([]), np.array([], dtype=bool)), np.array([])),
        ((np.arange(4).reshape(2, 2), np.eye(2, dtype=bool)), np.array([0, 3])),
    ],
)
def test_filter_array(args, expected):
    result = m.filter_array(*args)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([[1, 3], [5, 7]]), 0), {"sum": [6, 10], "mean": [3, 5], "max": [5, 7]}),
        ((np.array([1, 3]), -1), {"sum": 4, "mean": 2, "max": 3}),
        (
            (np.ones((2, 3, 4)), 1),
            {"sum": np.full((2, 4), 3), "mean": np.ones((2, 4)), "max": np.ones((2, 4))},
        ),
    ],
)
def test_axis_statistics(args, expected):
    result = m.axis_statistics(*args)
    assert set(result) == set(expected)
    for key in expected:
        np.testing.assert_allclose(result[key], expected[key])


def test_statistics_empty():
    with pytest.raises(ValueError):
        m.axis_statistics(np.empty((0, 2)), 0)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([1]), np.array([2]), 0), np.array([1, 2])),
        ((np.empty((0, 2)), np.ones((1, 2)), 0), np.ones((1, 2))),
        ((np.ones((2, 1)), np.zeros((2, 1)), -1), np.array([[1, 0], [1, 0]])),
    ],
)
def test_combine_arrays(args, expected):
    result = m.combine_arrays(*args)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([2, 4, 6]),), [0, 0.5, 1]),
        ((np.empty((0, 2)),), np.empty((0, 2))),
        ((np.full((2, 2), 7),), np.zeros((2, 2))),
    ],
)
def test_normalize_array(args, expected):
    result = m.normalize_array(*args)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([0, 2]), 3), [[1, 0, 0], [0, 0, 1]]),
        ((np.array([], dtype=int), 2), np.empty((0, 2))),
        ((np.array([1, 1]), 2), [[0, 1], [0, 1]]),
    ],
)
def test_one_hot_encode(args, expected):
    result = m.one_hot_encode(*args)
    assert np.issubdtype(result.dtype, np.integer)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize("labels,c", [(np.array([-1]), 2), (np.array([2]), 2), (np.array([0]), 0)])
def test_one_hot_invalid(labels, c):
    with pytest.raises(ValueError):
        m.one_hot_encode(labels, c)
