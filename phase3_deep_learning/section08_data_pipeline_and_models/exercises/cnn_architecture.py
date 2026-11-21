"""Learner skeletons; no reference answers."""

from torch import Tensor, nn


def conv2d_output_size(
    input_size: int, kernel_size: int, stride: int = 1, padding: int = 0, dilation: int = 1
) -> int:
    """07. Conv Output Size. One spatial axis, floor((I+2P-D*(K-1)-1)/S+1); positive I/K/S/D, P>=0 and output>=1.
    Input Shape -> Output Shape: scalar I -> scalar O, apply separately to H/W
    Expected dtype: Python int
    Grad / computation graph: no graph
    Hint: Derive effective kernel size with dilation."""
    # TODO
    raise NotImplementedError


def build_cnn(in_channels: int, num_classes: int) -> nn.Module:
    """08. Build CNN. At least two Conv/ReLU blocks and pooling, adaptive final pooling to support varying sizes; output logits.
    Input Shape -> Output Shape: [B,C,H,W], H/W>=16 -> [B,K]
    Expected dtype: float32, model float32
    Grad / computation graph: trainable graph
    Hint: Avoid a Linear input size tied to 28x28."""
    # TODO
    raise NotImplementedError


def build_residual_block(channels: int) -> nn.Module:
    """09. Residual Block. Return same-shape block with output ReLU(x+F(x)); F contains two padded 3x3 convolutions and ReLU between them. No normalization required.
    Input Shape -> Output Shape: [B,C,H,W] -> same
    Expected dtype: float32
    Grad / computation graph: both skip and residual preserve gradient
    Hint: Use out-of-place addition; test F=0 and negative x."""
    # TODO
    raise NotImplementedError


def topk_accuracy(logits: Tensor, targets: Tensor, k: int) -> float:
    """10. Top K Accuracy. Fraction of samples whose label is among top k; require N>0 and 1<=k<=K.
    Input Shape -> Output Shape: [N,K],[N] -> float in [0,1]
    Expected dtype: float logits; long targets
    Grad / computation graph: metric must not retain graph
    Hint: Top-k along class axis, not batch axis."""
    # TODO
    raise NotImplementedError
