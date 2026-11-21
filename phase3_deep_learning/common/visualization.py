"""Headless learning curves, confusion matrices and misclassification galleries."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import DataLoader


def plot_history(history: list[dict], path: Path) -> None:
    """Plot sample-weighted epoch loss and accuracy."""
    figure, axes = plt.subplots(1, 2, figsize=(8, 3), layout="constrained")
    for axis, metric in zip(axes, ["loss", "accuracy"], strict=True):
        for prefix in ["train", "val"]:
            axis.plot(
                [r["epoch"] for r in history],
                [r[f"{prefix}_{metric}"] for r in history],
                label=prefix,
            )
        axis.set(xlabel="Epoch", ylabel=metric)
        axis.legend()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path)
    plt.close(figure)


def classification_artifacts(
    model: nn.Module, loader: DataLoader, device: torch.device, directory: Path, classes: int
) -> torch.Tensor:
    """Save confusion counts and up to nine errors; images are raw display samples."""
    directory.mkdir(parents=True, exist_ok=True)
    confusion = torch.zeros(classes, classes, dtype=torch.int64)
    errors: list[tuple] = []
    previous = model.training
    model.eval()
    try:
        with torch.inference_mode():
            for inputs, targets in loader:
                predictions = model(inputs.to(device)).argmax(1).cpu()
                indices = targets * classes + predictions
                confusion += torch.bincount(indices, minlength=classes**2).reshape(classes, classes)
                for x, y, pred in zip(inputs, targets, predictions, strict=True):
                    if y != pred and len(errors) < 9:
                        errors.append((x.cpu(), int(y), int(pred)))
    finally:
        model.train(previous)
    figure, axis = plt.subplots(figsize=(4, 4), layout="constrained")
    axis.imshow(confusion.numpy(), cmap="Blues")
    axis.set(xlabel="Predicted", ylabel="True", title="Confusion matrix")
    figure.savefig(directory / "confusion_matrix.png")
    plt.close(figure)
    import json

    (directory / "confusion_matrix.json").write_text(json.dumps(confusion.tolist()))
    figure, axes = plt.subplots(3, 3, figsize=(6, 6), layout="constrained")
    for axis in axes.flat:
        axis.axis("off")
    for axis, (image, true, pred) in zip(axes.flat, errors):
        image = image.permute(1, 2, 0).squeeze().numpy()
        low, high = float(image.min()), float(image.max())
        axis.imshow((image - low) / max(high - low, 1e-8), cmap="gray")
        axis.set_title(f"true={true}, pred={pred}", fontsize=8)
    if not errors:
        figure.suptitle("No misclassified samples")
    figure.savefig(directory / "errors.png")
    plt.close(figure)
    return confusion
