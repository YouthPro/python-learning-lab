"""Learner TODOs; project implementations do not import this module."""

from typing import Any

import numpy as np
import torch
from torch import Tensor


def create_tensor(data: Any, dtype: torch.dtype | None = None) -> Tensor:
    """01. Tensor Factory.

    Copy input into a new CPU tensor; dtype=None uses Torch inference. No alias to source storage.
    Input Shape -> Output Shape: rectangular data [*S] -> [*S]
    Expected dtype: inferred or explicit dtype
    Grad / computation graph: new leaf, requires_grad=False
    Hint: Compare tensor construction with as_tensor; validate dtype in tests.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def transform_tensor(x: Tensor, shape: tuple[int, ...]) -> Tensor:
    """02. Shape Transformation.

    Reshape, allowing one inferred -1; support non-contiguous inputs.
    Input Shape -> Output Shape: [*S], same element count -> [*shape]
    Expected dtype: same as x
    Grad / computation graph: preserve autograd connection for floating input
    Hint: Think about when view requires contiguous memory.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def add_batch_dim(x: Tensor, dim: int = 0) -> Tensor:
    """03. Add Batch Dimension.

    Insert one singleton axis, including negative dimensions; do not remove existing axes.
    Input Shape -> Output Shape: [d0,...] -> singleton inserted at dim
    Expected dtype: same as x
    Grad / computation graph: preserve computation graph
    Hint: Read the legal range of unsqueeze dimensions.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def normalize_last_dim(x: Tensor, eps: float = 1e-8) -> Tensor:
    """04. Last Dimension Normalization.

    Normalize each last-axis row with population std (correction=0), dividing by std clamped below by eps. Constants become zeros; eps>0.
    Input Shape -> Output Shape: [...,D], D>=1 -> same
    Expected dtype: floating input, preserve dtype
    Grad / computation graph: preserve graph; avoid in-place operations
    Hint: Keep reduced axes for broadcasting; explain singleton std.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def select_rows(x: Tensor, mask: Tensor) -> Tensor:
    """05. Masked Row Selection.

    Select rows using a bool [N] mask; preserve row order.
    Input Shape -> Output Shape: [N,*S] and [N] -> [M,*S]
    Expected dtype: x dtype; mask bool
    Grad / computation graph: selected values retain gradient paths
    Hint: Check mask length and dtype; M may be zero.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def pairwise_cosine_similarity(x: Tensor, y: Tensor) -> Tensor:
    """06. Pairwise Cosine Similarity.

    Return all pairwise cosines; zero-norm vectors have similarity zero using norm clamp 1e-8.
    Input Shape -> Output Shape: [N,D], [M,D] -> [N,M]
    Expected dtype: matching floating dtype
    Grad / computation graph: preserve both input graphs
    Hint: Sketch matrix multiplication axes before coding.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def move_to_device(data: Any, device: str | torch.device) -> Any:
    """07. Recursive Device Transfer.

    Transfer tensors recursively in dict/list/tuple; keep structure, keys and non-tensor leaves. Do not mutate input containers.
    Input Shape -> Output Shape: nested tensor [*S] -> identical shapes
    Expected dtype: preserve each tensor dtype
    Grad / computation graph: Tensor.to preserves graph; CPU->CPU may return same tensor
    Hint: Use type checks; strings must not be treated as sequences.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def to_numpy(tensor: Tensor) -> np.ndarray:
    """08. NumPy Interoperability.

    Return detached independent CPU NumPy copy. bfloat16 converts to float32; other NumPy-compatible dtypes preserved.
    Input Shape -> Output Shape: [*S] -> numpy [*S]
    Expected dtype: NumPy equivalent, bfloat16 -> float32
    Grad / computation graph: explicitly detach; returned array has no graph
    Hint: Explain why direct numpy fails on requires_grad=True or CUDA.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError
