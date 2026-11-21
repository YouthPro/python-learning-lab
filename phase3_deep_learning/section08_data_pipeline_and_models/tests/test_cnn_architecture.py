import pytest
import torch
from torch import nn

from phase3_deep_learning.section08_data_pipeline_and_models.exercises import cnn_architecture as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "args,expected", [((28, 3), 26), ((32, 3, 2, 1), 16), ((17, 3, 1, 2, 2), 17)]
)
def test_conv2d_output_size(args, expected):
    assert m.conv2d_output_size(*args) == expected


@pytest.mark.parametrize("shape", [(2, 1, 28, 28), (3, 1, 32, 40), (1, 1, 16, 16)])
def test_build_cnn(shape):
    model = m.build_cnn(1, 4)
    out = model(torch.randn(shape))
    assert out.shape == (shape[0], 4) and out.requires_grad
    assert sum(isinstance(layer, nn.Conv2d) for layer in model.modules()) >= 2
    out.sum().backward()
    assert any(p.grad is not None for p in model.parameters())


@pytest.mark.parametrize("channels", [1, 3, 8])
def test_build_residual_block(channels):
    model = m.build_residual_block(channels)
    assert sum(isinstance(layer, nn.Conv2d) for layer in model.modules()) == 2
    for parameter in model.parameters():
        nn.init.zeros_(parameter)
    x = torch.randn(2, channels, 8, 9, requires_grad=True)
    out = model(x)
    torch.testing.assert_close(out, x.relu())
    out.sum().backward()
    assert x.grad is not None
    with torch.no_grad():
        for parameter in model.parameters():
            parameter.fill_(0.1)
    positive = torch.ones(2, channels, 8, 9)
    assert (model(positive) > positive).any()


@pytest.mark.parametrize("k,expected", [(1, 0.5), (2, 1.0), (3, 1.0)])
def test_topk_accuracy(k, expected):
    logits = torch.tensor([[3.0, 2.0, 1.0], [3.0, 2.0, 1.0]], requires_grad=True)
    assert m.topk_accuracy(logits, torch.tensor([0, 1]), k) == expected
