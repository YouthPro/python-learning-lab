"""FashionMNIST CNN with a real, reproducible multi-configuration comparison."""

import argparse
import csv
import json
from pathlib import Path
from time import perf_counter
from typing import Any

import torch
from torch.utils.data import DataLoader

from phase3_deep_learning.common.data import fashion_splits, split_three, synthetic_images
from phase3_deep_learning.common.engine import evaluate_model
from phase3_deep_learning.common.experiment import fit_classifier
from phase3_deep_learning.common.models import MLP
from phase3_deep_learning.common.runtime import choose_device, seed_all
from phase3_deep_learning.common.visualization import classification_artifacts

from .models import CNN


def run(
    output: Path,
    *,
    synthetic: bool = False,
    download: bool = False,
    data_root: Path = Path("datasets/raw/fashion_mnist"),
    epochs: int = 3,
    seed: int = 42,
    device: str = "cpu",
    model_kind: str = "cnn",
    depth: int = 2,
    batch_size: int = 64,
    learning_rate: float = 0.001,
    dropout: float = 0.2,
) -> dict:
    """Train one controlled comparison sample, selecting weights on validation loss."""
    if synthetic and download:
        raise ValueError("synthetic mode never downloads")
    seed_all(seed)
    target = choose_device(device)
    splits = (
        split_three(synthetic_images(180, classes=10, seed=seed), seed)
        if synthetic
        else fashion_splits(data_root, download=download, seed=seed)
    )
    train, validation, test = splits
    train_loader = DataLoader(
        train, batch_size=batch_size, shuffle=True, generator=torch.Generator().manual_seed(seed)
    )
    val_loader, test_loader = (DataLoader(s, batch_size=batch_size) for s in [validation, test])
    if model_kind not in {"mlp", "cnn"}:
        raise ValueError("model_kind must be mlp or cnn")
    model = (
        CNN(1, 10, depth, dropout)
        if model_kind == "cnn"
        else MLP([1, 28, 28], [128], 10, dropout=dropout)
    )
    spec = {
        "kind": model_kind,
        "input_shape": [1, 28, 28],
        "num_classes": 10,
        "depth": depth,
        "dropout": dropout,
    }
    if model_kind == "mlp":
        spec.update(hidden_dims=[128], activation="relu")
    started = perf_counter()
    history = fit_classifier(
        model,
        train_loader,
        val_loader,
        output,
        spec,
        target,
        epochs=epochs,
        learning_rate=learning_rate,
    )
    elapsed = perf_counter() - started
    test_metrics = evaluate_model(model, test_loader, target)
    classification_artifacts(model, test_loader, target, output, 10)
    result = {
        "model": model_kind,
        "depth": depth,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "dropout": dropout,
        "val_loss": min(h["val_loss"] for h in history),
        "test_accuracy": test_metrics["accuracy"],
        "duration": elapsed,
        "parameters": sum(p.numel() for p in model.parameters()),
        "synthetic": synthetic,
    }
    (output / "result.json").write_text(json.dumps(result, indent=2))
    return result


def compare(output: Path, **kwargs: Any) -> list[dict]:
    """Vary one factor against baseline; report actual measurements, never presets."""
    experiments = [
        dict(model_kind="mlp"),
        {},
        {"depth": 3},
        {"batch_size": 32},
        {"learning_rate": 0.01},
        {"dropout": 0.4},
    ]
    rows = [
        run(output / f"experiment_{i}", **dict(kwargs, **changes))
        for i, changes in enumerate(experiments)
    ]
    with (output / "comparison.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = "# Actual CNN comparison\n\nSynthetic mode measures pipeline behavior, not FashionMNIST performance.\n\n"
    report += "| model | depth | batch | lr | dropout | val loss | test acc | seconds |\n|---|---|---|---|---|---|---|---|\n"
    for row in rows:
        report += (
            f"| {row['model']} | {row['depth']} | {row['batch_size']} | {row['learning_rate']} | "
            f"{row['dropout']} | {row['val_loss']:.5f} | {row['test_accuracy']:.4f} | {row['duration']:.3f} |\n"
        )
    (output / "comparison.md").write_text(report)
    return rows


def main() -> None:
    """Expose single-run and comparison entry points."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--dropout", type=float, default=0.2)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--data-root", type=Path, default=Path("datasets/raw/fashion_mnist"))
    parser.add_argument("--output", type=Path, default=Path("outputs/phase3/cnn"))
    args = vars(parser.parse_args())
    torch.set_num_threads(2)
    output, comparison = args.pop("output"), args.pop("compare")
    print(json.dumps(compare(output, **args) if comparison else run(output, **args)))


if __name__ == "__main__":
    main()
