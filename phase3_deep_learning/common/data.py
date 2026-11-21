"""Small synthetic image data and explicit-only FashionMNIST access."""

from pathlib import Path

import torch
from torch.utils.data import Dataset, Subset, TensorDataset


def synthetic_images(
    samples: int = 240, channels: int = 1, size: int = 28, classes: int = 3, seed: int = 42
) -> TensorDataset:
    """Generate noisy class-specific vertical patches, using a local RNG."""
    if samples < 1 or size < classes or channels not in {1, 3} or classes < 2:
        raise ValueError("invalid synthetic data dimensions")
    generator = torch.Generator().manual_seed(seed)
    labels = torch.arange(samples) % classes
    inputs = torch.rand(samples, channels, size, size, generator=generator) * 0.15
    width = max(1, size // classes)
    for index, label in enumerate(labels):
        start = int(label) * width
        inputs[index, :, :, start : start + width] += 0.8
    order = torch.randperm(samples, generator=generator)
    return TensorDataset(inputs[order].float(), labels[order].long())


def split_three(
    dataset: Dataset, seed: int = 42, val_ratio: float = 0.15, test_ratio: float = 0.15
) -> tuple[Subset, Subset, Subset]:
    """Return disjoint train/validation/test subsets with persisted-able indices."""
    if val_ratio <= 0 or test_ratio <= 0 or val_ratio + test_ratio >= 1:
        raise ValueError("invalid split ratios")
    count = len(dataset)
    validation, test = max(1, int(count * val_ratio)), max(1, int(count * test_ratio))
    if count - validation - test < 1:
        raise ValueError("at least three samples are required")
    order = torch.randperm(count, generator=torch.Generator().manual_seed(seed)).tolist()
    return (
        Subset(dataset, order[validation + test :]),
        Subset(dataset, order[:validation]),
        Subset(dataset, order[validation : validation + test]),
    )


def fashion_splits(
    root: str | Path, *, download: bool = False, seed: int = 42
) -> tuple[Dataset, Dataset, Dataset]:
    """Load real FashionMNIST; no network access unless download=True."""
    from torchvision.datasets import FashionMNIST
    from torchvision.transforms import Compose, Normalize, ToTensor

    transform = Compose([ToTensor(), Normalize((0.5,), (0.5,))])
    train = FashionMNIST(str(root), train=True, transform=transform, download=download)
    test = FashionMNIST(str(root), train=False, transform=transform, download=download)
    order = torch.randperm(len(train), generator=torch.Generator().manual_seed(seed)).tolist()
    n_val = max(1, int(0.15 * len(train)))
    return Subset(train, order[n_val:]), Subset(train, order[:n_val]), test
