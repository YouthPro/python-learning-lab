"""Gradient-free, sample-weighted validation and checkpoint model loading."""

from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader

from phase3_deep_learning.common.engine import evaluate_model

from ..models import build_model
from ..utils.checkpoint import load_checkpoint


def load_model(path: str | Path, device: torch.device) -> tuple[nn.Module, dict]:
    """Rebuild architecture from data-only metadata; no datasets/weights downloaded."""
    state = load_checkpoint(path)
    model = build_model(state["model_spec"]).to(device)
    model.load_state_dict(state["model"])
    model.eval()
    return model, state


def evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> dict:
    """Return loss/accuracy/sample count without modifying model parameters."""
    return evaluate_model(model, loader, device)
