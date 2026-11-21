"""Model shapes and independent train/validation inputs."""

import pytest
import torch
from training_framework.config import validate_config
from training_framework.datasets import build_data
from training_framework.models import build_model

from phase3_deep_learning.section08_data_pipeline_and_models.projects.image_dataset_pipeline.src.generate import (
    generate_images,
)


@pytest.mark.parametrize("kind", ["mlp", "cnn"])
def test_forward_backward(kind, tmp_path):
    c = validate_config({"run_dir": str(tmp_path), "model": {"name": kind}})
    model = build_model(c["model"])
    output = model(torch.rand(4, 1, 16, 16))
    assert output.shape == (4, 3)
    output.sum().backward()
    assert all(p.grad is not None for p in model.parameters())


def test_synthetic_reproducibility(tmp_path):
    c = validate_config({"run_dir": str(tmp_path), "data": {"samples": 50}})
    a, b = build_data(c), build_data(c)
    assert a.fingerprint == b.fingerprint
    assert not set(a.train.dataset.indices) & set(a.validation.dataset.indices)
    xa, ya = next(iter(a.train))
    xb, yb = next(iter(b.train))
    torch.testing.assert_close(xa, xb)
    torch.testing.assert_close(ya, yb)
    assert xa.dtype == torch.float32 and ya.dtype == torch.long and not a.train.pin_memory


def test_custom_folder_and_fingerprint(tmp_path):
    root = generate_images(tmp_path / "images", 3)
    c = validate_config(
        {
            "run_dir": str(tmp_path / "run"),
            "data": {"kind": "image_folder", "root": str(root)},
            "model": {"input_shape": [3, 16, 16]},
        }
    )
    data = build_data(c)
    assert data.classes == ["bird", "cat", "dog"] and data.preprocess["normalize"] == "imagenet"
    x, _ = next(iter(data.validation))
    assert x.shape[1:] == (3, 16, 16)
    target = root / "bird/generated_000.png"
    target.write_bytes((root / "cat/generated_000.png").read_bytes())
    assert build_data(c).fingerprint != data.fingerprint
