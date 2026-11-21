import pytest
import torch
from PIL import Image
from torch import nn
from torchvision.models import resnet18

from phase3_deep_learning.section08_data_pipeline_and_models.exercises import transfer_learning as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("training,classes", [(True, 2), (False, 5), (True, 7)])
def test_freeze_backbone(training, classes):
    model = resnet18(weights=None)
    model.fc = nn.Linear(512, classes)
    model.train(training)
    assert m.freeze_backbone(model) is model
    assert all(p.requires_grad == name.startswith("fc.") for name, p in model.named_parameters())
    assert model.training == training


@pytest.mark.parametrize("n", [0, 1, 4])
def test_unfreeze_last_n_blocks(n):
    model = resnet18(weights=None)
    assert m.unfreeze_last_n_blocks(model, n) is model
    allowed = {"fc"} | {f"layer{i}" for i in range(5 - n, 5)}
    assert all(
        p.requires_grad == (name.split(".")[0] in allowed) for name, p in model.named_parameters()
    )


@pytest.mark.parametrize("classes", [2, 3, 7])
def test_replace_classifier(classes):
    model = resnet18(weights=None)
    before = model.conv1.weight.detach().clone()
    assert m.replace_classifier(model, classes) is model
    assert (
        model.fc.in_features == 512
        and model.fc.out_features == classes
        and model.fc.weight.requires_grad
    )
    torch.testing.assert_close(before, model.conv1.weight)


@pytest.mark.parametrize(
    "training,size,mode", [(True, 32, "RGB"), (False, 24, "L"), (False, 48, "RGBA")]
)
def test_build_transforms(training, size, mode):
    transform = m.build_transforms(size, training)
    image = Image.new(mode, (70, 60))
    out = transform(image)
    assert out.shape == (3, size, size) and out.dtype == torch.float32 and torch.isfinite(out).all()
    if not training:
        torch.testing.assert_close(out, transform(image))


@pytest.mark.parametrize("batch_size", [1, 2, 5])
def test_predict_batch(batch_size):
    class Guard(nn.Module):
        def forward(self, x):
            assert not torch.is_grad_enabled() and not self.training
            return x.mean((2, 3))

    model = Guard()
    model.train()
    inputs = torch.randn(batch_size, 3, 8, 8)
    out = m.predict_batch(model, inputs, "cpu")
    assert (
        out.shape == (batch_size, 3)
        and out.device.type == "cpu"
        and not out.requires_grad
        and model.training
    )
    torch.testing.assert_close(out.sum(1), torch.ones(batch_size))
    torch.testing.assert_close(out, inputs.mean((2, 3)).softmax(1))
