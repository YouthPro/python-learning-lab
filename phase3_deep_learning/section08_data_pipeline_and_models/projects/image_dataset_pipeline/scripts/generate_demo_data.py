"""Run as a module from the repository root."""

import argparse
from pathlib import Path

from ..src.generate import generate_images


def main() -> None:
    """Create local example class directories."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("outputs/phase3/demo_images"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generate_images(args.root, seed=args.seed)


if __name__ == "__main__":
    main()
