"""Learner skeletons; no reference answers."""

from typing import Callable

import torch
from torch import Tensor, nn


def freeze_backbone(model: nn.Module) -> nn.Module:
    """11. Freeze Backbone. ResNet-style model: freeze every parameter except fc; fc remains trainable; return same model. Mode unchanged.
    Input Shape -> Output Shape: module -> unchanged
    Expected dtype: parameter dtypes preserved
    Grad / computation graph: backbone requires_grad=False, head=True
    Hint: Frozen parameters and frozen BatchNorm running stats are distinct."""
    # TODO
    raise NotImplementedError


def unfreeze_last_n_blocks(model: nn.Module, n: int) -> nn.Module:
    """12. Unfreeze Last Blocks. Reset backbone frozen; unfreeze last n of layer1..layer4, n in [0,4]; fc trainable, stem stays frozen. Return model.
    Input Shape -> Output Shape: module -> unchanged
    Expected dtype: parameter dtypes preserved
    Grad / computation graph: last n stages and head track parameter grads
    Hint: n=0 must not accidentally select all via [-0:]."""
    # TODO
    raise NotImplementedError


def replace_classifier(model: nn.Module, num_classes: int) -> nn.Module:
    """13. Replace Classifier. Replace ResNet fc with trainable Linear(old in_features,K), keep device/dtype and other parameters.
    Input Shape -> Output Shape: old logits[B,1000] -> [B,K]
    Expected dtype: preserve model dtype/device
    Grad / computation graph: new head trainable
    Hint: Do not hard-code feature width; no network request."""
    # TODO
    raise NotImplementedError


def build_transforms(image_size: int, training: bool) -> Callable:
    """14. Build Image Transforms. PIL RGB conversion; training random resized crop/flip, evaluation deterministic resize; ToTensor and ImageNet mean/std.
    Input Shape -> Output Shape: PIL arbitrary grayscale/RGB -> [3,S,S]
    Expected dtype: float32
    Grad / computation graph: input transform has no autograd graph
    Hint: Train/val must not share random augmentation; ImageNet weights expect matching normalization."""
    # TODO
    raise NotImplementedError


def predict_batch(model: nn.Module, batch: Tensor, device: str | torch.device) -> Tensor:
    """15. Predict Batch. Return CPU softmax probabilities, no gradients; preserve previous train/eval mode.
    Input Shape -> Output Shape: [B,C,H,W] -> [B,K]
    Expected dtype: float32 by default
    Grad / computation graph: no graph
    Hint: eval alone does not disable gradients."""
    # TODO
    raise NotImplementedError
