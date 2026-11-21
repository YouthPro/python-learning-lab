"""Checkpoint metadata is sufficient for a fresh model and a single local image."""

import pytest
import torch
from PIL import Image
from training_framework.config import validate_config
from training_framework.engine.evaluator import load_model
from training_framework.engine.predictor import predict_image
from training_framework.engine.trainer import Trainer
from training_framework.utils.checkpoint import load_checkpoint


@pytest.mark.parametrize("model", ["mlp", "cnn"])
def test_image_prediction_and_schema(tmp_path, model):
    config = validate_config(
        {
            "run_dir": str(tmp_path),
            "data": {"samples": 30},
            "model": {"name": model},
            "training": {"epochs": 1},
        }
    )
    Trainer(config).fit()
    image = tmp_path / "sample.jpg"
    Image.new("RGB", (27, 35), (255, 0, 0)).save(image)
    result = predict_image(tmp_path / "checkpoints/best.pt", image)
    assert (
        result["label"] in ["class_0", "class_1", "class_2"] and len(result["probabilities"]) == 3
    )
    assert abs(sum(result["probabilities"]) - 1) < 1e-6
    restored, state = load_model(tmp_path / "checkpoints/best.pt", torch.device("cpu"))
    assert not restored.training and state["preprocess"]["channels"] == 1


def test_safe_loading_rejects_module_pickle(tmp_path):
    path = tmp_path / "unsafe.pt"
    torch.save(torch.nn.Linear(2, 2), path)
    import pickle

    with pytest.raises(pickle.UnpicklingError):
        load_checkpoint(path)
