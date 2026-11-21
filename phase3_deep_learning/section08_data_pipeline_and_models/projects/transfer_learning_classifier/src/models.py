"""ResNet18 and explicit head/stage/full fine-tuning strategies."""

from torch import nn
from torchvision.models import ResNet18_Weights, resnet18


def make_resnet(classes: int, *, pretrained: bool = False) -> nn.Module:
    """Only pretrained=True may fetch weights; inference always passes False."""
    if classes < 2:
        raise ValueError("at least two classes required")
    model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1 if pretrained else None)
    model.fc = nn.Linear(model.fc.in_features, classes)
    return model


def set_strategy(model: nn.Module, strategy: str) -> nn.Module:
    """A=head only, B=last stage+head, C=all; rebuild optimizer after changing."""
    if strategy not in {"A", "B", "C"}:
        raise ValueError("strategy must be A/B/C")
    model.requires_grad_(strategy == "C")
    model.fc.requires_grad_(True)
    if strategy == "B":
        model.layer4.requires_grad_(True)
    return model
