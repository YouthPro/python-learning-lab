"""Generate optional demo images and inspect a custom directory DataLoader."""

import argparse
import json
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from phase3_deep_learning.common.runtime import seed_worker

from .dataset import prepare_pipeline
from .generate import generate_images


def main() -> None:
    """An image directory is read-only unless --generate-demo is explicitly passed."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("outputs/phase3/demo_images"))
    parser.add_argument("--output", type=Path, default=Path("outputs/phase3/image_manifest.json"))
    parser.add_argument("--generate-demo", action="store_true")
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.generate_demo:
        generate_images(args.root, seed=args.seed)
    train, validation, manifest = prepare_pipeline(args.root, args.output, seed=args.seed)
    loader = DataLoader(
        train,
        batch_size=8,
        num_workers=args.workers,
        worker_init_fn=seed_worker,
        generator=torch.Generator().manual_seed(args.seed),
    )
    x, y = next(iter(loader))
    print(
        json.dumps(
            {
                "train": len(train),
                "val": len(validation),
                "shape": list(x.shape),
                "labels": y.tolist(),
                "corrupt": manifest["errors"],
            }
        )
    )


if __name__ == "__main__":
    main()
