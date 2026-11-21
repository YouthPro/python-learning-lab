"""Actual CPU training; optional AMP never invokes CUDA on a CPU run."""

import csv
import json

import pytest
from training_framework.config import validate_config
from training_framework.engine.trainer import Trainer
from training_framework.utils.checkpoint import load_checkpoint


@pytest.mark.parametrize("model", ["mlp", "cnn"])
def test_training_outputs_and_modes(tmp_path, model):
    c = validate_config(
        {
            "run_dir": str(tmp_path),
            "model": {"name": model},
            "data": {"samples": 60},
            "training": {"epochs": 2, "batch_size": 13, "amp": True},
        }
    )
    history = Trainer(c).fit()
    assert len(history) == 2 and all(not r["amp_enabled"] for r in history)
    assert all(r["train_samples"] == 48 and r["val_samples"] == 12 for r in history)
    assert all(0 <= r["val_accuracy"] <= 1 and r["epoch_duration"] > 0 for r in history)
    rows = [json.loads(s) for s in (tmp_path / "logs/metrics.jsonl").read_text().splitlines()]
    with (tmp_path / "logs/metrics.csv").open() as handle:
        csv_rows = list(csv.DictReader(handle))
    assert len(rows) == len(csv_rows) == 2 and [r["epoch"] for r in rows] == [1, 2]
    latest = load_checkpoint(tmp_path / "checkpoints/latest.pt")
    best = load_checkpoint(tmp_path / "checkpoints/best.pt")
    assert latest["epoch"] == 2 and best["best_metric"] == min(r["val_loss"] for r in rows)
    assert latest["optimizer"]["state"] and latest["scheduler"]["last_epoch"] == 2
    assert (tmp_path / "outputs/learning_curves.png").stat().st_size > 0
    with pytest.raises(FileExistsError):
        Trainer(c).fit()
