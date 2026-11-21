"""Convolution blocks with adaptive spatial pooling and logits output."""

import torch
from torch import nn


class ConvBlock(nn.Sequential):
    """Convolution, normalization, activation, downsampling and regularization."""

    def __init__(self, inputs: int, outputs: int, dropout: float) -> None:
        super().__init__(
            nn.Conv2d(inputs, outputs, 3, padding=1),
            nn.BatchNorm2d(outputs),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(dropout),
        )


class CNN(nn.Module):
    """Support variable image sizes (minimum 2**depth) with a 2x2 feature head."""

    def __init__(
        self, in_channels: int = 1, num_classes: int = 10, depth: int = 2, dropout: float = 0.2
    ) -> None:
        super().__init__()
        if depth not in {1, 2, 3} or not 0 <= dropout < 1 or in_channels < 1 or num_classes < 2:
            raise ValueError("invalid CNN dimensions/depth/dropout")
        blocks = []
        width = in_channels
        for index in range(depth):
            next_width = 16 * 2**index
            blocks.append(ConvBlock(width, next_width, dropout))
            width = next_width
        self.features = nn.Sequential(*blocks, nn.AdaptiveAvgPool2d((2, 2)))
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Dropout(dropout), nn.Linear(width * 4, num_classes)
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """Return [B,K] logits, not probabilities."""
        return self.classifier(self.features(inputs))
