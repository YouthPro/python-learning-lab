"""Separate data construction, deterministic split and DataLoader factories."""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Subset

from phase3_deep_learning.common.runtime import choose_device

from ..seed import seed_worker
from .image_folder import DirectoryImages, image_transforms, scan_images
from .synthetic import make_synthetic


@dataclass
class DataBundle:
    """Training and validation data plus inference and resume metadata."""

    train: DataLoader
    validation: DataLoader
    classes: list[str]
    preprocess: dict
    fingerprint: str

    def save_split(self, run_dir: str | Path, seed: int) -> None:
        """Persist the actual subset indices after validating a resume request."""
        out = Path(run_dir) / "outputs"
        out.mkdir(parents=True, exist_ok=True)
        (out / "split.json").write_text(
            json.dumps(
                {
                    "train": self.train.dataset.indices,
                    "validation": self.validation.dataset.indices,
                    "classes": self.classes,
                    "seed": seed,
                },
                indent=2,
            )
        )


def build_data(config: dict, *, persist_split: bool = True) -> DataBundle:
    """Use separate transform objects; fingerprint content and exact split."""
    d, m = config["data"], config["model"]
    seed = config["seed"]
    root = Path(d["root"]) if d["root"] else None
    digest = hashlib.sha256()
    if d["kind"] == "synthetic":
        train_data = make_synthetic(d["samples"], m["input_shape"], m["num_classes"], seed)
        val_data = train_data
        for tensor in train_data.tensors:
            digest.update(tensor.numpy().tobytes())
        classes = [f"class_{i}" for i in range(m["num_classes"])]
        normalize = "none"
    else:
        manifest = scan_images(root)
        classes = manifest["classes"]
        if len(classes) != m["num_classes"]:
            raise ValueError("num_classes must match sorted folder labels")
        train_data = DirectoryImages(
            root, manifest["records"], image_transforms(m["input_shape"][1], True)
        )
        val_data = DirectoryImages(
            root, manifest["records"], image_transforms(m["input_shape"][1], False)
        )
        for record in manifest["records"]:
            digest.update(record["path"].encode())
            digest.update((root / record["path"]).read_bytes())
        normalize = "imagenet"
    order = torch.randperm(len(train_data), generator=torch.Generator().manual_seed(seed)).tolist()
    n_val = max(1, int(len(order) * d["val_ratio"]))
    if n_val >= len(order):
        raise ValueError("split leaves no training samples")
    indices = {"train": order[n_val:], "validation": order[:n_val]}
    digest.update(json.dumps(indices, sort_keys=True).encode())
    options = {
        "batch_size": config["training"]["batch_size"],
        "num_workers": d["num_workers"],
        "pin_memory": choose_device(config["device"]).type == "cuda",
        "worker_init_fn": seed_worker,
    }
    train = DataLoader(
        Subset(train_data, indices["train"]),
        shuffle=True,
        generator=torch.Generator().manual_seed(seed),
        **options,
    )
    val = DataLoader(
        Subset(val_data, indices["validation"]),
        shuffle=False,
        generator=torch.Generator().manual_seed(seed + 1),
        **options,
    )
    bundle = DataBundle(
        train,
        val,
        classes,
        {
            "channels": m["input_shape"][0],
            "image_size": m["input_shape"][1],
            "normalize": normalize,
        },
        digest.hexdigest(),
    )
    if persist_split:
        bundle.save_split(config["run_dir"], seed)
    return bundle
