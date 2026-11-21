"""Train nonlinear circles; save learning curves and a held-out decision boundary."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader

from phase3_deep_learning.common.data import split_three
from phase3_deep_learning.common.engine import evaluate_model, probabilities
from phase3_deep_learning.common.experiment import fit_classifier
from phase3_deep_learning.common.runtime import choose_device, seed_all

from .data import make_circles
from .models import MLP


def run(
    output: Path,
    *,
    samples: int = 6000,
    epochs: int = 15,
    seed: int = 42,
    hidden_dims: list[int] | None = None,
    activation: str = "relu",
    learning_rate: float = 0.01,
    optimizer: str = "adam",
    device: str = "cpu",
) -> dict:
    """Complete train/val/test experiment with explicit model metadata."""
    seed_all(seed)
    target = choose_device(device)
    dataset = make_circles(samples, seed)
    train, validation, test = split_three(dataset, seed)
    generator = torch.Generator().manual_seed(seed)
    train_loader = DataLoader(train, batch_size=128, shuffle=True, generator=generator)
    val_loader, test_loader = (DataLoader(s, batch_size=128) for s in [validation, test])
    spec = {
        "kind": "mlp",
        "input_shape": [2],
        "hidden_dims": hidden_dims or [32, 32],
        "num_classes": 2,
        "activation": activation,
        "dropout": 0.0,
    }
    model = MLP(**{k: v for k, v in spec.items() if k != "kind"})
    history = fit_classifier(
        model,
        train_loader,
        val_loader,
        output,
        spec,
        target,
        epochs=epochs,
        learning_rate=learning_rate,
        optimizer_name=optimizer,
    )
    result = evaluate_model(model, test_loader, target)
    axis = torch.linspace(-2, 2, 150)
    xx, yy = torch.meshgrid(axis, axis, indexing="xy")
    grid = torch.stack([xx.flatten(), yy.flatten()], 1)
    predicted = torch.cat([probabilities(model, batch, target) for batch in grid.split(1024)])
    figure, axes = plt.subplots(figsize=(5, 4), layout="constrained")
    axes.contourf(xx.numpy(), yy.numpy(), predicted[:, 1].reshape(150, 150).numpy(), alpha=0.6)
    x, y = dataset.tensors
    indices = test.indices
    axes.scatter(x[indices, 0], x[indices, 1], c=y[indices], s=5, edgecolors="none")
    axes.set(title="Held-out test points and learned boundary", xlabel="x1", ylabel="x2")
    figure.savefig(output / "decision_boundary.png")
    plt.close(figure)
    (output / "splits.json").write_text(
        json.dumps(
            {
                "seed": seed,
                "train": train.indices,
                "validation": validation.indices,
                "test": indices,
            }
        )
    )
    (output / "test_metrics.json").write_text(json.dumps(result))
    return {"history": history, "test": result, "samples": samples}


def main() -> None:
    """Expose architecture/optimizer/LR comparisons without downloading data."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("outputs/phase3/mlp"))
    parser.add_argument("--samples", type=int, default=6000)
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--hidden", type=int, nargs="+", default=[32, 32])
    parser.add_argument("--activation", choices=["relu", "tanh", "gelu"], default="relu")
    parser.add_argument("--optimizer", choices=["adam", "sgd"], default="adam")
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    torch.set_num_threads(2)
    result = run(
        args.output,
        samples=args.samples,
        epochs=args.epochs,
        seed=args.seed,
        hidden_dims=args.hidden,
        activation=args.activation,
        learning_rate=args.learning_rate,
        optimizer=args.optimizer,
        device=args.device,
    )
    print(json.dumps(result["test"]))


if __name__ == "__main__":
    main()
