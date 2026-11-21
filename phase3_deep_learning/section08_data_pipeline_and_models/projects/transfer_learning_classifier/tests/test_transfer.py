"""Offline ResNet construction and lightweight strategy training/inference."""

import torch
from PIL import Image
from torch import nn

from phase3_deep_learning.common.engine import train_epoch
from phase3_deep_learning.section08_data_pipeline_and_models.projects.transfer_learning_classifier.src import (
    main as project,
)
from phase3_deep_learning.section08_data_pipeline_and_models.projects.transfer_learning_classifier.src.data import (
    datasets,
)
from phase3_deep_learning.section08_data_pipeline_and_models.projects.transfer_learning_classifier.src.models import (
    make_resnet,
    set_strategy,
)


class TinyResNet(nn.Module):
    """Small stage-shaped model, not a mocked optimizer or mocked training loop."""

    def __init__(self, classes=3):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 4, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(4)
        for name in ["layer1", "layer2", "layer3", "layer4"]:
            setattr(self, name, nn.Sequential(nn.Conv2d(4, 4, 3, padding=1), nn.ReLU()))
        self.fc = nn.Linear(4, classes)

    def forward(self, x):
        x = self.bn1(self.conv1(x))
        for name in ["layer1", "layer2", "layer3", "layer4"]:
            x = getattr(self, name)(x)
        return self.fc(x.mean((2, 3)))


def test_real_resnet_is_offline_and_has_correct_head():
    model = make_resnet(3, pretrained=False).eval()
    with torch.inference_mode():
        assert model(torch.rand(1, 3, 64, 64)).shape == (1, 3)


def test_frozen_backbone_and_bn_unchanged(tmp_path):
    model = set_strategy(TinyResNet(), "A")
    before = {k: v.clone() for k, v in model.state_dict().items()}
    dataset = torch.utils.data.TensorDataset(torch.rand(6, 3, 16, 16), torch.arange(6) % 3)
    train_epoch(
        model,
        torch.utils.data.DataLoader(dataset, batch_size=3),
        torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=0.01),
        torch.device("cpu"),
    )
    for name, value in model.state_dict().items():
        if not name.startswith("fc."):
            torch.testing.assert_close(value, before[name])
    assert not torch.equal(model.fc.weight, before["fc.weight"])


def test_full_strategy_comparison_and_single_image_inference(tmp_path, monkeypatch):
    monkeypatch.setattr(
        project, "make_resnet", lambda classes, pretrained=False: TinyResNet(classes)
    )
    rows = project.run(tmp_path, samples=12, epochs=1, image_size=32)
    counts = [r["trainable_parameters"] for r in rows]
    assert counts[0] < counts[1] < counts[2]
    assert all(0 <= r["val_accuracy"] <= 1 and r["training_seconds"] > 0 for r in rows)
    image = tmp_path / "input.png"
    Image.new("L", (30, 40), 127).save(image)
    result = project.infer(tmp_path / "B/best.pt", image)
    assert len(result["probabilities"]) == 3
    assert abs(sum(result["probabilities"]) - 1) < 1e-6


def test_rgb_adaptation_and_disjoint_eval():
    train, val, classes = datasets("synthetic", root=None, samples=12, image_size=24)
    assert not set(train.indices) & set(val.indices)
    assert val[0][0].shape == (3, 24, 24) and len(classes) == 3
    torch.testing.assert_close(val[0][0], val[0][0])
