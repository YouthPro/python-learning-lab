"""Native Torch batch loops; no learner exercise implementations are imported."""

import torch
from torch import nn
from torch.utils.data import DataLoader

from .metrics import RunningMetrics


def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    *,
    accumulation_steps: int = 1,
    max_norm: float | None = None,
    amp: bool = False,
    scaler: torch.amp.GradScaler | None = None,
) -> dict[str, float | int]:
    """Train CE classification, normalizing accumulated gradients by sample count.

    AMP is CUDA-only. Frozen BatchNorm layers retain their running statistics.
    A final incomplete accumulation window is stepped with its actual denominator.
    """
    if accumulation_steps < 1 or (max_norm is not None and max_norm <= 0):
        raise ValueError("invalid accumulation_steps or max_norm")
    model.train()
    for module in model.modules():
        if isinstance(module, nn.modules.batchnorm._BatchNorm) and not any(
            p.requires_grad for p in module.parameters()
        ):
            module.eval()
    enabled = amp and device.type == "cuda"
    scaler = scaler or torch.amp.GradScaler("cuda", enabled=enabled)
    metrics = RunningMetrics()
    optimizer.zero_grad(set_to_none=True)
    window_samples = 0
    for index, (inputs, targets) in enumerate(loader):
        inputs, targets = inputs.to(device), targets.to(device)
        with torch.autocast(device_type=device.type, enabled=enabled):
            logits = model(inputs)
            loss = nn.functional.cross_entropy(logits, targets)
        if not torch.isfinite(loss):
            raise ValueError("non-finite training loss")
        count = targets.numel()
        scaler.scale(loss * count).backward()
        window_samples += count
        metrics.update(loss.item(), int((logits.argmax(1) == targets).sum().item()), count)
        if (index + 1) % accumulation_steps == 0 or index + 1 == len(loader):
            scaler.unscale_(optimizer)
            for parameter in model.parameters():
                if parameter.grad is not None:
                    parameter.grad.div_(window_samples)
            if max_norm is not None:
                nn.utils.clip_grad_norm_(model.parameters(), max_norm)
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad(set_to_none=True)
            window_samples = 0
    return metrics.result()


def evaluate_model(
    model: nn.Module, loader: DataLoader, device: torch.device
) -> dict[str, float | int]:
    """Evaluate without gradients and restore the caller's previous model mode."""
    previous = model.training
    model.eval()
    metrics = RunningMetrics()
    try:
        with torch.inference_mode():
            for inputs, targets in loader:
                inputs, targets = inputs.to(device), targets.to(device)
                logits = model(inputs)
                loss = nn.functional.cross_entropy(logits, targets)
                metrics.update(
                    loss.item(), int((logits.argmax(1) == targets).sum().item()), targets.numel()
                )
    finally:
        model.train(previous)
    return metrics.result()


def probabilities(model: nn.Module, inputs: torch.Tensor, device: torch.device) -> torch.Tensor:
    """Predict detached CPU [N,K] probabilities, preserving the prior mode."""
    previous = model.training
    model.eval()
    try:
        with torch.inference_mode():
            return model(inputs.to(device)).softmax(1).cpu()
    finally:
        model.train(previous)
