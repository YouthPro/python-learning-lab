"""Engineering learner TODOs; no full exercise solutions."""

from pathlib import Path
from typing import Any

import torch
from torch import nn


def save_checkpoint(
    path: str | Path,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: Any,
    epoch: int,
    best_metric: float,
) -> None:
    """08. Save Checkpoint. Save model/optimizer/scheduler state_dicts, epoch and best_metric. Never serialize entire model. Create parent directory.
    Input Shape -> Output Shape: parameter tensors -> file
    Expected dtype: tensors+primitive containers
    Grad / computation graph: saved states not computational graph
    Hint: Keep schema keys explicit; scheduler may be None."""
    # TODO
    raise NotImplementedError


def load_checkpoint(
    path: str | Path,
    model: nn.Module,
    optimizer: torch.optim.Optimizer | None = None,
    scheduler: Any = None,
    device: str = "cpu",
) -> dict[str, Any]:
    """09. Load Checkpoint. torch.load with explicit weights_only=True/map_location; restore supplied objects and return loaded metadata. Do not load arbitrary pickled modules.
    Input Shape -> Output Shape: file -> restored shapes + metadata
    Expected dtype: model dtypes unchanged
    Grad / computation graph: no forward graph
    Hint: state_dict restores parameters; restoring optimizer/scheduler is separate."""
    # TODO
    raise NotImplementedError


def log_experiment(metrics: dict[str, Any], path: str | Path) -> None:
    """10. JSONL Experiment Logger. Append exactly one UTF-8 JSON object and newline, preserve existing records, reject non-finite JSON floats.
    Input Shape -> Output Shape: metric mapping -> one line
    Expected dtype: JSON primitives
    Grad / computation graph: convert values beforehand; no graph storage
    Hint: Serialize before appending so invalid records do not partially corrupt a log."""
    # TODO
    raise NotImplementedError
