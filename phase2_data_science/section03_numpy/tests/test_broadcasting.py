import numpy as np
import pytest

import phase2_data_science.section03_numpy.exercises.broadcasting as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([[1, 2], [3, 2]]),), [[-1, 0], [1, 0]]),
        ((np.empty((0, 3)),), np.empty((0, 3))),
        ((np.ones((1, 2, 3)),), np.zeros((1, 2, 3))),
    ],
)
def test_normalize_batch(args, expected):
    result = m.normalize_batch(*args)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([[0, 0]]), np.array([[3, 4]])), [[5]]),
        ((np.empty((0, 2)), np.ones((3, 2))), np.empty((0, 3))),
        ((np.zeros((2, 1, 3)), np.ones((2, 4, 3))), np.full((2, 1, 4), np.sqrt(3))),
    ],
)
def test_pairwise_distance(args, expected):
    result = m.pairwise_distance(*args)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([-1, 2, 8]), 0, 5), [0, 2, 5]),
        ((np.array([]), 0, 1), []),
        ((np.array([[1, 2], [3, 4]]), 2, 3), [[2, 2], [3, 3]]),
    ],
)
def test_clip_values(args, expected):
    result = m.clip_values(*args)
    np.testing.assert_allclose(result, expected)


def test_clip_invalid():
    with pytest.raises(ValueError):
        m.clip_values(np.array([1]), 2, 1)
