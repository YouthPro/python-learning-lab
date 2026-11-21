"""FashionMNIST MLP architecture (28x28 grayscale to ten logits)."""

from phase3_deep_learning.common.models import MLP


def make_model(hidden_dims: list[int] | None = None) -> MLP:
    """Build a reference image MLP without loading data or weights."""
    return MLP([1, 28, 28], hidden_dims or [128, 64], 10)
