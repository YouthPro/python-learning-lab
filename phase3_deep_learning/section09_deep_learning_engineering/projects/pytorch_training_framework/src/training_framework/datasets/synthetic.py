"""Generated image classification data without downloads."""

from torch.utils.data import TensorDataset

from phase3_deep_learning.common.data import synthetic_images


def make_synthetic(samples: int, shape: list[int], classes: int, seed: int) -> TensorDataset:
    """Return CPU float32 images and int64 class labels."""
    return synthetic_images(samples, shape[0], shape[1], classes, seed)
