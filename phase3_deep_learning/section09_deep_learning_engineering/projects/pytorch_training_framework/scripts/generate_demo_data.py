"""Generate directory images and one prediction sample; no internet."""

import argparse
from pathlib import Path

from phase3_deep_learning.section08_data_pipeline_and_models.projects.image_dataset_pipeline.src.generate import (
    generate_images,
)


def main() -> None:
    """Generate a reproducible three-class image directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("outputs/demo_images"))
    parser.add_argument("--sample", type=Path, default=Path("sample.jpg"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generate_images(args.root, seed=args.seed)
    from PIL import Image

    args.sample.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(args.root / "bird/generated_000.png") as image:
        image.save(args.sample)


if __name__ == "__main__":
    main()
