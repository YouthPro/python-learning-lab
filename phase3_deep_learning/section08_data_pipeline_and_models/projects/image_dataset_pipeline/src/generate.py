"""Generate repeatable local RGB fixtures; never delete custom user images."""

import json
from pathlib import Path

import numpy as np
from PIL import Image


def generate_images(root: Path, samples_per_class: int = 12, seed: int = 42) -> Path:
    """Overwrite only generated_*.png files of these deterministic sample names."""
    if samples_per_class < 1:
        raise ValueError("samples_per_class must be positive")
    rng = np.random.default_rng(seed)
    colors = [(220, 25, 25), (25, 210, 25), (25, 25, 220)]
    for name, color in zip(["bird", "cat", "dog"], colors, strict=True):
        folder = root / name
        folder.mkdir(parents=True, exist_ok=True)
        for index in range(samples_per_class):
            array = np.empty((36, 40, 3), dtype=np.int16)
            array[:] = color
            array += rng.integers(-12, 13, array.shape, dtype=np.int16)
            Image.fromarray(array.clip(0, 255).astype(np.uint8)).save(
                folder / f"generated_{index:03d}.png"
            )
    (root / "generation.json").write_text(
        json.dumps({"seed": seed, "per_class": samples_per_class})
    )
    return root
