"""Offline nonlinear two-dimensional classification data."""

import numpy as np
import torch
from torch.utils.data import TensorDataset


def make_circles(samples: int = 6000, seed: int = 42) -> TensorDataset:
    """Generate >=5000 samples by default; smaller sizes are explicit smoke fixtures."""
    if samples < 3:
        raise ValueError("samples must be >=3")
    rng = np.random.default_rng(seed)
    labels = np.arange(samples) % 2
    angles = rng.uniform(0, 2 * np.pi, samples)
    radii = np.where(labels == 0, 0.5, 1.3) + rng.normal(0, 0.12, samples)
    inputs = np.column_stack([radii * np.cos(angles), radii * np.sin(angles)])
    order = rng.permutation(samples)
    return TensorDataset(
        torch.from_numpy(inputs[order].astype("float32")),
        torch.from_numpy(labels[order].astype("int64")),
    )
