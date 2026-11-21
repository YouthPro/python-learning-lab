"""Reference MLP; input flattening is explicit and independent of exercises."""

import math

from torch import Tensor, nn


class MLP(nn.Module):
    """Batch-first classifier producing unnormalized [B,K] logits."""

    def __init__(
        self,
        input_shape: list[int],
        hidden_dims: list[int],
        num_classes: int,
        activation: str = "relu",
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        if activation not in {"relu", "tanh", "gelu"}:
            raise ValueError("activation must be relu, tanh or gelu")
        if (
            not input_shape
            or min(input_shape) < 1
            or num_classes < 2
            or any(d < 1 for d in hidden_dims)
        ):
            raise ValueError("invalid model dimensions")
        if not 0 <= dropout < 1:
            raise ValueError("dropout must lie in [0,1)")
        layers: list[nn.Module] = [nn.Flatten()]
        width = math.prod(input_shape)
        for hidden in hidden_dims:
            layers.extend(
                [
                    nn.Linear(width, hidden),
                    {"relu": nn.ReLU, "tanh": nn.Tanh, "gelu": nn.GELU}[activation](),
                ]
            )
            if dropout:
                layers.append(nn.Dropout(dropout))
            width = hidden
        layers.append(nn.Linear(width, num_classes))
        self.network = nn.Sequential(*layers)

    def forward(self, inputs: Tensor) -> Tensor:
        """Return logits; CrossEntropyLoss performs its own log-softmax."""
        return self.network(inputs)
