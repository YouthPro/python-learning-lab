"""Dataset adapters for RGB ImageNet transfer inputs, with explicit downloads."""

from pathlib import Path

import torch
from PIL import Image
from torch.utils.data import Dataset, Subset
from torchvision.datasets import CIFAR10, FashionMNIST

from phase3_deep_learning.common.data import synthetic_images
from phase3_deep_learning.section08_data_pipeline_and_models.projects.image_dataset_pipeline.src.dataset import (
    DirectoryImages,
    image_transforms,
    scan_images,
)


class AdaptedSynthetic(Dataset):
    """Apply the same RGB transforms used by real images to generated data."""

    def __init__(self, seed: int, samples: int, size: int, training: bool) -> None:
        self.data = synthetic_images(samples, channels=3, size=32, classes=3, seed=seed)
        self.transform = image_transforms(size, training)

    def __len__(self) -> int:
        """Return sample count."""
        return len(self.data)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        """Convert generated CHW tensor to PIL before preprocessing."""
        tensor, label = self.data[index]
        image = Image.fromarray((tensor.permute(1, 2, 0).numpy() * 255).astype("uint8"))
        return self.transform(image), label


def datasets(
    kind: str,
    root: Path,
    *,
    download: bool = False,
    seed: int = 42,
    samples: int = 96,
    image_size: int = 224,
) -> tuple[Dataset, Dataset, list[str]]:
    """Return disjoint train/validation with independent train/eval transforms."""
    if kind == "synthetic":
        if download:
            raise ValueError("synthetic mode does not download")
        train_data = AdaptedSynthetic(seed, samples, image_size, True)
        val_data = AdaptedSynthetic(seed, samples, image_size, False)
        classes = ["class_0", "class_1", "class_2"]
    elif kind in {"fashion_mnist", "cifar10"}:
        factory = FashionMNIST if kind == "fashion_mnist" else CIFAR10
        train_data = factory(
            str(root), train=True, download=download, transform=image_transforms(image_size, True)
        )
        val_data = factory(
            str(root), train=True, download=download, transform=image_transforms(image_size, False)
        )
        classes = list(train_data.classes)
    elif kind == "folder":
        if download:
            raise ValueError("custom folders do not download")
        manifest = scan_images(root)
        train_data = DirectoryImages(root, manifest["records"], image_transforms(image_size, True))
        val_data = DirectoryImages(root, manifest["records"], image_transforms(image_size, False))
        classes = manifest["classes"]
    else:
        raise ValueError("unknown dataset")
    if len(train_data) < 4:
        raise ValueError("at least four examples required")
    order = torch.randperm(len(train_data), generator=torch.Generator().manual_seed(seed)).tolist()
    n_val = max(1, int(0.2 * len(order)))
    return Subset(train_data, order[n_val:]), Subset(val_data, order[:n_val]), classes
