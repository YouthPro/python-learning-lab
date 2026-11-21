"""CNN architecture, trained checkpoint, and actual comparison report checks."""

import json

import pytest
import torch

from phase3_deep_learning.common.checkpoint import load_state
from phase3_deep_learning.section08_data_pipeline_and_models.projects.cnn_image_classifier.src.main import (
    compare,
    run,
)
from phase3_deep_learning.section08_data_pipeline_and_models.projects.cnn_image_classifier.src.models import (
    CNN,
)


@pytest.mark.parametrize("shape", [(2, 1, 28, 28), (3, 1, 32, 40), (1, 3, 16, 16)])
def test_variable_input_shape(shape):
    model = CNN(shape[1], 4)
    logits = model(torch.rand(shape))
    assert logits.shape == (shape[0], 4)
    logits.sum().backward()
    assert all(p.grad is not None for p in model.parameters())


def test_train_checkpoint_and_confusion(tmp_path):
    result = run(tmp_path, synthetic=True, epochs=2)
    assert 0 <= result["test_accuracy"] <= 1
    assert sum(map(sum, json.loads((tmp_path / "confusion_matrix.json").read_text()))) == 27
    state = load_state(tmp_path / "best.pt")
    model = CNN(1, 10, state["model_spec"]["depth"], state["model_spec"]["dropout"])
    model.load_state_dict(state["model"])
    assert model(torch.rand(2, 1, 28, 28)).shape == (2, 10)


def test_comparison_varies_each_requested_factor(tmp_path):
    rows = compare(tmp_path, synthetic=True, epochs=1)
    assert len(rows) == 6
    assert {r["model"] for r in rows} == {"mlp", "cnn"}
    for key in ["depth", "batch_size", "learning_rate", "dropout"]:
        assert len({r[key] for r in rows}) == 2
    assert (tmp_path / "comparison.csv").stat().st_size > 0
    assert "Actual CNN comparison" in (tmp_path / "comparison.md").read_text()
