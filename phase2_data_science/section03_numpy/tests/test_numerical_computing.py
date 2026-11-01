import numpy as np
import pytest

import phase2_data_science.section03_numpy.exercises.numerical_computing as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([1, 0]), np.array([1, 0])), 1),
        ((np.array([0.0, 0.0]), np.array([1.0, 0.0])), 0),
        ((np.array([[1, 0], [-1, 0]]), np.array([1, 0])), [1, -1]),
        ((np.array([]), np.array([])), 0),
    ],
)
def test_cosine_similarity(args, expected):
    result = m.cosine_similarity(*args)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.array([1000.0, 1000.0]),), [0.5, 0.5]),
        ((np.empty((0, 2)),), np.empty((0, 2))),
        ((np.zeros((2, 3, 4)), 1), np.full((2, 3, 4), 1 / 3)),
    ],
)
def test_softmax(args, expected):
    result = m.softmax(*args)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize("size", [0, 5, (2, 3)])
def test_sample(size):
    np.random.seed(123)
    state = np.random.get_state()
    actual = m.sample_data(42, size)
    np.testing.assert_allclose(actual, np.random.default_rng(42).standard_normal(size))
    after = np.random.get_state()
    np.testing.assert_array_equal(state[1], after[1])
    assert state[2:] == after[2:]


@pytest.mark.parametrize(
    "args, expected",
    [
        ((np.ones((2, 3)), np.ones((3, 4))), np.full((2, 4), 3)),
        ((np.empty((0, 3)), np.ones((3, 2))), np.empty((0, 2))),
        ((np.ones((2, 1, 3)), np.ones((3, 4))), np.full((2, 1, 4), 3)),
    ],
)
def test_batch_matmul(args, expected):
    result = m.batch_matmul(*args)
    np.testing.assert_allclose(result, expected)
