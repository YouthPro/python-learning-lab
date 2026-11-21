"""Allowlisted architectures for both training and checkpoint inference."""

from torch import nn

from .cnn import CNN
from .mlp import MLP


def build_model(spec: dict) -> nn.Module:
    """Select MLP or CNN; never execute a user-provided import string."""
    if spec["name"] == "mlp":
        return MLP(
            spec["input_shape"],
            spec["hidden_dims"],
            spec["num_classes"],
            spec["activation"],
            spec["dropout"],
        )
    if spec["name"] == "cnn":
        return CNN(spec["input_shape"][0], spec["num_classes"], spec["depth"], spec["dropout"])
    raise ValueError("unsupported checkpoint model")
