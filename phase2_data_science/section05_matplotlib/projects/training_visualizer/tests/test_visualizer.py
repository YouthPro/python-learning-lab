import numpy as np
import pytest

from phase2_data_science.section05_matplotlib.projects.training_visualizer.src.training_visualizer import (
    detect_overfitting,
    load_log,
    visualize,
)
from scripts.generate_datasets import training_logs


@pytest.mark.parametrize("epochs", [1, 10, 50])
def test_visualizer(tmp_path, epochs):
    training_logs(tmp_path, epochs=epochs)
    a = load_log(tmp_path / "training_log.csv")
    b = load_log(tmp_path / "training_log_b.csv")
    assert len(a["epoch"]) == epochs
    report = visualize({"a": a, "b": b}, tmp_path / "out")
    assert set(report) == {"a", "b"}
    assert (tmp_path / "out/training_comparison.png").read_bytes().startswith(b"\x89PNG")


@pytest.mark.parametrize(
    "train,val,expected",
    [
        ([5, 4, 3, 2], [1, 2, 3, 4], [{"start_epoch": 2.0, "end_epoch": 4.0}]),
        ([5, 4, 3], [3, 2, 1], []),
        ([], [], []),
    ],
)
def test_intervals(train, val, expected):
    log = {
        "epoch": np.arange(1, len(train) + 1),
        "train_loss": np.array(train),
        "val_loss": np.array(val),
    }
    assert detect_overfitting(log, patience=3) == expected
