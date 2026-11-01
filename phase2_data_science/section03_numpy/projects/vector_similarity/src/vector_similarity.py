"""2D/3D batched vectors; query chunking limits pairwise temporary allocations."""

import argparse
import json
from pathlib import Path
from time import perf_counter

import numpy as np


def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    vectors = np.asarray(vectors, dtype=float)
    if vectors.ndim not in (1, 2, 3) or not np.isfinite(vectors).all():
        raise ValueError("expected finite 1D, 2D or 3D vectors")
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)


def pairwise(
    vectors: np.ndarray, queries: np.ndarray, metric: str = "cosine", chunk_size: int = 128
) -> np.ndarray:
    """(...,N,D),(...,Q,D) -> (...,Q,N); cosine returns similarity, others distance."""
    vectors = np.asarray(vectors, dtype=float)
    queries = np.asarray(queries, dtype=float)
    if queries.ndim == 1:
        queries = queries[None, :]
    if (
        vectors.ndim not in (2, 3)
        or queries.ndim not in (2, 3)
        or vectors.shape[-1] != queries.shape[-1]
    ):
        raise ValueError("incompatible vector shapes")
    if chunk_size <= 0 or metric not in {"cosine", "euclidean", "manhattan"}:
        raise ValueError("invalid metric or chunk size")
    if not np.isfinite(vectors).all() or not np.isfinite(queries).all():
        raise ValueError("finite vectors required")
    batch = np.broadcast_shapes(vectors.shape[:-2], queries.shape[:-2])
    vectors = np.broadcast_to(vectors, (*batch, *vectors.shape[-2:]))
    queries = np.broadcast_to(queries, (*batch, *queries.shape[-2:]))
    output = np.empty((*batch, queries.shape[-2], vectors.shape[-2]), dtype=float)
    normalized = normalize_vectors(vectors) if metric == "cosine" else vectors
    for start in range(0, queries.shape[-2], chunk_size):
        query = queries[..., start : start + chunk_size, :]
        if metric == "cosine":
            values = normalize_vectors(query) @ normalized.swapaxes(-1, -2)
            values = np.clip(values, -1, 1)
        elif metric == "euclidean":
            squared = (
                np.sum(query**2, axis=-1, keepdims=True)
                + np.sum(vectors**2, axis=-1)[..., None, :]
                - 2 * (query @ vectors.swapaxes(-1, -2))
            )
            values = np.sqrt(np.maximum(squared, 0))
        else:
            values = np.abs(query[..., :, None, :] - vectors[..., None, :, :]).sum(axis=-1)
        output[..., start : start + chunk_size, :] = values
    return output


def top_k(
    vectors: np.ndarray, queries: np.ndarray, k: int, metric: str = "cosine", chunk_size: int = 128
) -> tuple[np.ndarray, np.ndarray]:
    """Return indices and scores (...,Q,min(k,N)); tie breaks by input index."""
    if k < 0:
        raise ValueError("k must be nonnegative")
    # Chunk here as well so retrieval never allocates the entire Q x N result matrix.
    queries = np.asarray(queries)
    if queries.ndim == 1:
        queries = queries[None, :]
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    indices = []
    scores = []
    for start in range(0, max(queries.shape[-2], 1), chunk_size):
        matrix = pairwise(vectors, queries[..., start : start + chunk_size, :], metric, chunk_size)
        order = np.argsort(-matrix if metric == "cosine" else matrix, axis=-1, kind="stable")[
            ..., :k
        ]
        indices.append(order)
        scores.append(np.take_along_axis(matrix, order, axis=-1))
    return np.concatenate(indices, axis=-2), np.concatenate(scores, axis=-2)


def benchmark(vectors: np.ndarray, query: np.ndarray) -> dict:
    start = perf_counter()
    loop = np.array([float(normalize_vectors(v) @ normalize_vectors(query)) for v in vectors])
    loop_seconds = perf_counter() - start
    start = perf_counter()
    result = pairwise(vectors, query)[0]
    vector_seconds = perf_counter() - start
    np.testing.assert_allclose(loop, result, atol=1e-12)
    return {"loop_seconds": loop_seconds, "vector_seconds": vector_seconds}


def main(argv=None):
    p = argparse.ArgumentParser(description="Vector similarity and timing comparison")
    p.add_argument("--input", default="datasets/generated/vectors.npy")
    p.add_argument("--output", default="datasets/processed/vector_similarity.json")
    p.add_argument("--k", type=int, default=5)
    args = p.parse_args(argv)
    try:
        vectors = np.load(args.input, allow_pickle=False)
        query = vectors[0]
        indices, scores = top_k(vectors, query, args.k)
        report = {
            "indices": indices.tolist(),
            "scores": scores.tolist(),
            **benchmark(vectors, query),
        }
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2), encoding="utf-8")
    except (OSError, ValueError, IndexError) as exc:
        p.exit(2, f"{exc}\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
