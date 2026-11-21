"""Resumed training must match uninterrupted training, including dropout/shuffle."""

import json

import pytest
import torch
from training_framework.config import validate_config
from training_framework.engine.trainer import Trainer
from training_framework.utils.checkpoint import load_checkpoint


def config(path, epochs):
    return validate_config(
        {
            "run_dir": str(path),
            "data": {"samples": 47},
            "model": {"dropout": 0.2},
            "training": {"epochs": epochs, "batch_size": 7, "gradient_accumulation": 3},
        }
    )


def test_exact_resume_and_log_repair(tmp_path):
    full, partial = tmp_path / "full", tmp_path / "resumed"
    full_rows = Trainer(config(full, 3)).fit()
    Trainer(config(partial, 1)).fit()
    (partial / "logs/metrics.jsonl").write_text("incomplete crash artifact")
    resumed = Trainer(config(partial, 3)).fit(partial / "checkpoints/latest.pt")
    a, b = (load_checkpoint(p / "checkpoints/latest.pt") for p in [full, partial])
    for name, value in a["model"].items():
        torch.testing.assert_close(value, b["model"][name], rtol=0, atol=0)
    assert a["scheduler"] == b["scheduler"] and a["best_epoch"] == b["best_epoch"]
    assert a["early_stopping"] == b["early_stopping"]
    for left, right in zip(full_rows, resumed, strict=True):
        for key in ["train_loss", "val_loss", "train_accuracy", "val_accuracy", "learning_rate"]:
            assert left[key] == right[key]
    assert [
        json.loads(s)["epoch"] for s in (partial / "logs/metrics.jsonl").read_text().splitlines()
    ] == [1, 2, 3]


def test_resume_rejects_changed_hyperparameter(tmp_path):
    c = config(tmp_path, 1)
    Trainer(c).fit()
    split = tmp_path / "outputs/split.json"
    original_split = split.read_bytes()
    c["optimizer"]["lr"] = 0.3
    c["seed"] += 1
    c["training"]["epochs"] = 2
    with pytest.raises(ValueError, match="differs"):
        Trainer(c).fit(tmp_path / "checkpoints/latest.pt")
    assert split.read_bytes() == original_split


def test_resume_keeps_early_stopping_state(tmp_path):
    c = config(tmp_path, 1)
    Trainer(c).fit()
    path = tmp_path / "checkpoints/latest.pt"
    state = load_checkpoint(path)
    state["early_stopping"]["bad_epochs"] = 8
    torch.save(state, path)
    c["training"]["epochs"] = 4
    history = Trainer(c).fit(path)
    assert len(history) == 1
