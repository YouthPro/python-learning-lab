"""Real training and saved-model inference on an offline nonlinear problem."""

import torch

from phase3_deep_learning.common.checkpoint import load_state
from phase3_deep_learning.common.models import MLP
from phase3_deep_learning.section07_pytorch_fundamentals.projects.mlp_classifier.src.data import (
    make_circles,
)
from phase3_deep_learning.section07_pytorch_fundamentals.projects.mlp_classifier.src.train import (
    run,
)


def test_default_data_size_and_reproducibility():
    first, second = make_circles(), make_circles()
    assert len(first) >= 5000
    assert first.tensors[0].shape == (6000, 2)
    assert first.tensors[1].dtype == torch.long
    torch.testing.assert_close(first.tensors[0], second.tensors[0])


def test_model_shape_and_gradient():
    model = MLP([2], [8, 4], 2)
    out = model(torch.ones(3, 2))
    assert out.shape == (3, 2)
    out.sum().backward()
    assert all(p.grad is not None for p in model.parameters())


def test_train_artifacts_and_checkpoint_prediction(tmp_path):
    result = run(tmp_path, samples=600, epochs=5)
    assert result["history"][-1]["train_loss"] < result["history"][0]["train_loss"]
    assert result["test"]["samples"] == 90
    for name in [
        "best.pt",
        "latest.pt",
        "metrics.csv",
        "metrics.jsonl",
        "learning_curves.png",
        "decision_boundary.png",
        "splits.json",
        "test_metrics.json",
    ]:
        assert (tmp_path / name).stat().st_size > 0
    state = load_state(tmp_path / "best.pt")
    model = MLP(**{k: v for k, v in state["model_spec"].items() if k != "kind"})
    model.load_state_dict(state["model"])
    model.eval()
    probe = torch.tensor([[0.0, 0.0], [1.3, 0.0]])
    first = model(probe).detach()
    model.load_state_dict(load_state(tmp_path / "best.pt")["model"])
    torch.testing.assert_close(first, model(probe))
