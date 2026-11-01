import numpy as np
import pytest

from phase2_data_science.section03_numpy.projects.vector_similarity.src.vector_similarity import (
    benchmark,
    normalize_vectors,
    pairwise,
    top_k,
)


@pytest.mark.parametrize("shape", [(5, 3), (2, 5, 3), (0, 3)])
def test_shapes(shape):
    rng = np.random.default_rng(7)
    vectors = rng.normal(size=shape)
    query = rng.normal(size=(*shape[:-2], 4, 3))
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    np.testing.assert_allclose(normalize_vectors(vectors), vectors / norms)
    for metric in ["cosine", "euclidean", "manhattan"]:
        result = pairwise(vectors, query, metric, chunk_size=2)
        expected = (
            normalize_vectors(query) @ normalize_vectors(vectors).swapaxes(-1, -2)
            if metric == "cosine"
            else np.linalg.norm(query[..., :, None, :] - vectors[..., None, :, :], axis=-1)
            if metric == "euclidean"
            else np.abs(query[..., :, None, :] - vectors[..., None, :, :]).sum(-1)
        )
        np.testing.assert_allclose(result, expected, atol=1e-12)
        indices, scores = top_k(vectors, query, 2, metric, chunk_size=1)
        order = np.argsort(-expected if metric == "cosine" else expected, axis=-1, kind="stable")[
            ..., :2
        ]
        np.testing.assert_array_equal(indices, order)
        np.testing.assert_allclose(scores, np.take_along_axis(expected, order, -1), atol=1e-12)


@pytest.mark.parametrize("n", [1, 2, 5])
def test_zero_and_ties(n):
    v = np.zeros((n, 3))
    np.testing.assert_array_equal(normalize_vectors(v), v)
    i, s = top_k(v, np.zeros(3), n + 2)
    np.testing.assert_array_equal(i, [np.arange(n)])
    np.testing.assert_array_equal(s, np.zeros((1, n)))
    times = benchmark(np.ones((n, 3)), np.ones(3))
    assert all(value >= 0 for value in times.values())


@pytest.mark.parametrize("metric", ["cosine", "euclidean", "manhattan"])
def test_empty_queries(metric):
    indices, scores = top_k(np.ones((5, 3)), np.empty((0, 3)), 2, metric)
    assert indices.shape == scores.shape == (0, 2)
