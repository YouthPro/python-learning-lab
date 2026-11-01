"""Simulated training logs, without a deep learning runtime."""

import argparse
import csv
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLUMNS = ["epoch", "train_loss", "val_loss", "train_acc", "val_acc", "learning_rate"]


def load_log(path: str | Path) -> dict[str, np.ndarray]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != COLUMNS:
            raise ValueError(f"expected columns {COLUMNS}")
        rows = list(reader)
    result = {c: np.array([float(r[c]) for r in rows], dtype=float) for c in COLUMNS}
    if not all(np.isfinite(v).all() for v in result.values()):
        raise ValueError("log values must be finite")
    if len(result["epoch"]) and np.any(np.diff(result["epoch"]) <= 0):
        raise ValueError("epochs must be strictly increasing")
    return result


def detect_overfitting(
    log: dict[str, np.ndarray], patience: int = 3, min_delta: float = 0.0
) -> list[dict]:
    """Consecutive steps: train decreases and validation increases by > min_delta.

    An interval starts at the first worsening epoch and ends at the final worsening epoch.
    This is a heuristic, not a statistical test.
    """
    if patience <= 0 or min_delta < 0:
        raise ValueError("positive patience and nonnegative min_delta required")
    train, val = log["train_loss"], log["val_loss"]
    if len(train) != len(val) or len(train) != len(log["epoch"]):
        raise ValueError("log lengths differ")
    flags = (np.diff(train) < -min_delta) & (np.diff(val) > min_delta)
    intervals = []
    start = None
    for i, flag in enumerate([*flags, False]):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            if i - start >= patience:
                intervals.append(
                    {
                        "start_epoch": float(log["epoch"][start + 1]),
                        "end_epoch": float(log["epoch"][i]),
                    }
                )
            start = None
    return intervals


def visualize(logs: dict[str, dict], output: str | Path, patience: int = 3) -> dict:
    if not logs:
        raise ValueError("at least one experiment required")
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(3, 1, figsize=(9, 10), sharex=True)
    reports = {}
    try:
        for name, log in logs.items():
            for field, axis in [
                ("train_loss", axes[0]),
                ("val_loss", axes[0]),
                ("train_acc", axes[1]),
                ("val_acc", axes[1]),
                ("learning_rate", axes[2]),
            ]:
                axis.plot(log["epoch"], log[field], label=f"{name}: {field}")
            intervals = detect_overfitting(log, patience)
            reports[name] = intervals
            for interval in intervals:
                axes[0].axvspan(
                    interval["start_epoch"], interval["end_epoch"], alpha=0.12, color="red"
                )
        for ax, title, ylabel in zip(
            axes,
            [
                "Training and validation loss",
                "Training and validation accuracy",
                "Learning rate schedule",
            ],
            ["Loss", "Accuracy", "Learning rate"],
        ):
            ax.set(title=title, xlabel="Epoch", ylabel=ylabel)
            ax.legend()
        fig.tight_layout()
        fig.savefig(root / "training_comparison.png", dpi=150)
    finally:
        plt.close(fig)
    (root / "overfitting.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
    (root / "report.md").write_text(
        "# Training comparison\n\n![Training curves](training_comparison.png)\n\n红色区间表示训练 loss 下降且验证 loss 连续上升达到 patience 的候选过拟合区间。详见 overfitting.json。该规则只用于诊断提示。\n",
        encoding="utf-8",
    )
    return reports


def main(argv=None):
    p = argparse.ArgumentParser(description="Training log visualization and experiment comparison")
    p.add_argument("paths", nargs="+")
    p.add_argument("--output", default="datasets/processed/training_visualizer")
    p.add_argument("--patience", type=int, default=3)
    args = p.parse_args(argv)
    try:
        names = [Path(path).stem for path in args.paths]
        if len(names) != len(set(names)):
            raise ValueError("experiment stems must be unique")
        logs = {name: load_log(path) for name, path in zip(names, args.paths)}
        report = visualize(logs, args.output, args.patience)
    except (OSError, ValueError, KeyError) as exc:
        p.exit(2, f"{exc}\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
