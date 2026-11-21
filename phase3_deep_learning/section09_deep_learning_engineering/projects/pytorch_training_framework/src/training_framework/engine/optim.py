"""Optimizer and scheduler configuration factories."""

import torch
from torch import nn


def build_optimizer(model: nn.Module, config: dict) -> torch.optim.Optimizer:
    """Include trainable parameters only."""
    parameters = [p for p in model.parameters() if p.requires_grad]
    options = {"lr": config["lr"], "weight_decay": config["weight_decay"]}
    if config["name"] == "adam":
        return torch.optim.Adam(parameters, **options)
    if config["name"] == "sgd":
        return torch.optim.SGD(parameters, momentum=config["momentum"], **options)
    raise ValueError("unknown optimizer")


def build_scheduler(
    optimizer: torch.optim.Optimizer, config: dict
) -> torch.optim.lr_scheduler.LRScheduler | torch.optim.lr_scheduler.ReduceLROnPlateau | None:
    """Plateau consumes validation loss; StepLR consumes completed epochs."""
    if config["name"] == "none":
        return None
    if config["name"] == "step":
        return torch.optim.lr_scheduler.StepLR(optimizer, config["step_size"], config["gamma"])
    if config["name"] == "plateau":
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, factor=config["gamma"], patience=config["patience"]
        )
    raise ValueError("unknown scheduler")
