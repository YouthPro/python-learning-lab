"""A deliberately small complete reference-project training driver."""

from pathlib import Path
from time import perf_counter

import torch
from torch import nn
from torch.utils.data import DataLoader

from .checkpoint import load_state, save_state
from .engine import evaluate_model, train_epoch
from .logging import write_history
from .visualization import plot_history


def fit_classifier(
    model: nn.Module,
    train: DataLoader,
    validation: DataLoader,
    output: Path,
    spec: dict,
    device: torch.device,
    *,
    epochs: int = 5,
    learning_rate: float = 0.01,
    optimizer_name: str = "adam",
) -> list[dict]:
    """Train, log and save best/latest state dicts; select using validation only."""
    if epochs < 1 or learning_rate <= 0 or optimizer_name not in {"adam", "sgd"}:
        raise ValueError("invalid training hyperparameters")
    model.to(device)
    parameters = [p for p in model.parameters() if p.requires_grad]
    optimizer = (
        torch.optim.Adam(parameters, lr=learning_rate)
        if optimizer_name == "adam"
        else torch.optim.SGD(parameters, lr=learning_rate, momentum=0.9)
    )
    history: list[dict] = []
    best = float("inf")
    for epoch in range(1, epochs + 1):
        started = perf_counter()
        train_result = train_epoch(model, train, optimizer, device)
        val_result = evaluate_model(model, validation, device)
        row = {
            "epoch": epoch,
            "train_loss": train_result["loss"],
            "val_loss": val_result["loss"],
            "train_accuracy": train_result["accuracy"],
            "val_accuracy": val_result["accuracy"],
            "learning_rate": learning_rate,
            "epoch_duration": perf_counter() - started,
        }
        history.append(row)
        state = {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": None,
            "epoch": epoch,
            "model_spec": spec,
            "history": history,
        }
        if val_result["loss"] < best:
            best = val_result["loss"]
            save_state(output / "best.pt", state)
        save_state(output / "latest.pt", state)
        write_history(history, output)
    plot_history(history, output / "learning_curves.png")
    model.load_state_dict(load_state(output / "best.pt")["model"])
    return history
