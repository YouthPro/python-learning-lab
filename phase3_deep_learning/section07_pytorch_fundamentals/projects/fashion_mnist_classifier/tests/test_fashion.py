"""Fashion project smoke uses generated tensors, never the online dataset."""

import json

import torch

from phase3_deep_learning.common.data import split_three, synthetic_images
from phase3_deep_learning.section07_pytorch_fundamentals.projects.fashion_mnist_classifier.src.models import (
    make_model,
)
from phase3_deep_learning.section07_pytorch_fundamentals.projects.fashion_mnist_classifier.src.train import (
    run,
)


def test_shape():
    model = make_model([16])
    assert model(torch.ones(4, 1, 28, 28)).shape == (4, 10)


def test_no_overlap():
    a, b, c = split_three(synthetic_images(60, classes=10))
    assert not (
        set(a.indices) & set(b.indices)
        or set(b.indices) & set(c.indices)
        or set(a.indices) & set(c.indices)
    )
    assert len(a) + len(b) + len(c) == 60


def test_offline_training_and_restore(tmp_path):
    result = run(tmp_path, synthetic=True, epochs=2, hidden_dims=[16])
    assert len(result["history"]) == 2 and result["test"]["samples"] == 36
    confusion = json.loads((tmp_path / "confusion_matrix.json").read_text())
    assert len(confusion) == 10 and sum(map(sum, confusion)) == 36
    assert (tmp_path / "errors.png").stat().st_size > 0
    out = torch.load(tmp_path / "predictions.pt", weights_only=True)
    assert out.shape == (36, 10) and not out.requires_grad
    torch.testing.assert_close(out.sum(1), torch.ones(36))
