"""A custom directory dataset with stable labels and image corruption checks."""

import json
from pathlib import Path
from typing import Callable

import torch
from PIL import Image, UnidentifiedImageError
from torch.utils.data import Dataset
from torchvision import transforms

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


class RGB:
    """Picklable transform (unlike lambdas) for grayscale/RGBA directory images."""

    def __call__(self, image: Image.Image) -> Image.Image:
        """Convert any supported image to three RGB channels."""
        return image.convert("RGB")


def image_transforms(
    size: int = 32, training: bool = False, imagenet: bool = True
) -> transforms.Compose:
    """Use augmentation only for training; evaluation is deterministic."""
    if size < 8:
        raise ValueError("image size must be >=8")
    operations: list = [RGB()]
    operations += (
        [transforms.RandomResizedCrop(size, scale=(0.8, 1.0)), transforms.RandomHorizontalFlip()]
        if training
        else (
            [transforms.Resize(256), transforms.CenterCrop(224)]
            if imagenet and size == 224
            else [transforms.Resize((size, size))]
        )
    )
    operations.append(transforms.ToTensor())
    if imagenet:
        operations.append(transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD))
    return transforms.Compose(operations)


def scan_images(root: str | Path) -> dict:
    """Decode/verify supported images; return valid records and explicit errors."""
    root = Path(root)
    if not root.is_dir():
        raise FileNotFoundError(root)
    classes = sorted(p.name for p in root.iterdir() if p.is_dir())
    records, errors = [], []
    for label, name in enumerate(classes):
        for path in sorted((root / name).rglob("*")):
            if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            try:
                with Image.open(path) as image:
                    image.verify()
                # verify and pixel decoding catch different forms of truncation.
                with Image.open(path) as image:
                    image.convert("RGB").load()
            except (UnidentifiedImageError, OSError, ValueError) as exc:
                errors.append({"path": path.relative_to(root).as_posix(), "error": str(exc)})
                continue
            records.append(
                {"path": path.relative_to(root).as_posix(), "label": label, "class_name": name}
            )
    if not records:
        raise ValueError("no valid images found")
    return {"classes": classes, "records": records, "errors": errors}


class DirectoryImages(Dataset):
    """Read a manifest subset without ImageFolder; optionally augment each sample."""

    def __init__(
        self, root: str | Path, records: list[dict], transform: Callable | None = None
    ) -> None:
        self.root = Path(root).resolve()
        self.records = records
        self.transform = transform or image_transforms(imagenet=False)
        for record in records:
            path = (self.root / record["path"]).resolve()
            if not path.is_relative_to(self.root):
                raise ValueError("manifest path escapes dataset root")

    def __len__(self) -> int:
        """Return manifest length."""
        return len(self.records)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        """Decode one image without leaving open PIL file handles."""
        record = self.records[index]
        with Image.open(self.root / record["path"]) as image:
            inputs = self.transform(image.convert("RGB"))
        return inputs, torch.tensor(record["label"], dtype=torch.long)


def prepare_pipeline(
    root: Path, output: Path, *, seed: int = 42, val_ratio: float = 0.2, size: int = 32
) -> tuple[DirectoryImages, DirectoryImages, dict]:
    """Persist exact splits, label order and class statistics; separate transforms."""
    if not 0 < val_ratio < 1:
        raise ValueError("val_ratio must be between 0 and 1")
    manifest = scan_images(root)
    records = manifest["records"]
    if len(records) < 2:
        raise ValueError("at least two images required")
    order = torch.randperm(len(records), generator=torch.Generator().manual_seed(seed)).tolist()
    n_val = min(len(records) - 1, max(1, int(len(records) * val_ratio)))
    validation, train = order[:n_val], order[n_val:]
    counts = torch.bincount(
        torch.tensor([records[i]["label"] for i in train]), minlength=len(manifest["classes"])
    )
    weights = torch.zeros(len(counts), dtype=torch.float32)
    present = counts > 0
    weights[present] = len(train) / (len(counts) * counts[present].float())
    manifest.update(
        seed=seed,
        train_indices=train,
        val_indices=validation,
        train_class_counts=counts.tolist(),
        train_class_weights=weights.tolist(),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return (
        DirectoryImages(root, [records[i] for i in train], image_transforms(size, True)),
        DirectoryImages(root, [records[i] for i in validation], image_transforms(size, False)),
        manifest,
    )
