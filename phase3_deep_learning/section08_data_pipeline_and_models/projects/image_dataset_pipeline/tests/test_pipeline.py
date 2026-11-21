"""Decode real generated images and exercise actual DataLoader collation."""

import hashlib

import torch
from torch.utils.data import DataLoader

from phase3_deep_learning.section08_data_pipeline_and_models.projects.image_dataset_pipeline.src.dataset import (
    prepare_pipeline,
    scan_images,
)
from phase3_deep_learning.section08_data_pipeline_and_models.projects.image_dataset_pipeline.src.generate import (
    generate_images,
)


def test_repeatable_generation_and_corruption(tmp_path):
    root = generate_images(tmp_path / "images", 3)
    hashes = {
        p.name + p.parent.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*.png")
    }
    generate_images(root, 3)
    assert hashes == {
        p.name + p.parent.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*.png")
    }
    (root / "cat/broken.png").write_bytes(b"not an image")
    manifest = scan_images(root)
    assert manifest["classes"] == ["bird", "cat", "dog"] and len(manifest["records"]) == 9
    assert len(manifest["errors"]) == 1


def test_independent_transforms_disjoint_reproducible_split(tmp_path):
    root = generate_images(tmp_path / "images", 4)
    train, val, manifest = prepare_pipeline(root, tmp_path / "splits.json", size=24)
    _, _, other = prepare_pipeline(root, tmp_path / "other.json", size=24)
    assert manifest == other
    assert not set(manifest["train_indices"]) & set(manifest["val_indices"])
    assert train.transform is not val.transform
    x, y = val[0]
    assert x.shape == (3, 24, 24) and y.dtype == torch.long
    torch.testing.assert_close(x, val[0][0])


def test_dataloader_worker_and_statistics(tmp_path):
    root = generate_images(tmp_path / "images", 5)
    train, _, manifest = prepare_pipeline(root, tmp_path / "splits.json")
    loader = DataLoader(train, batch_size=4, num_workers=1)
    batches = list(loader)
    assert sum(y.numel() for _, y in batches) == len(train)
    assert all(x.shape[1:] == (3, 32, 32) for x, _ in batches)
    assert sum(manifest["train_class_counts"]) == len(train)
    assert len(manifest["train_class_weights"]) == 3
