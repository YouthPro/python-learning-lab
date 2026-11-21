import pytest
import torch
from torch import nn

from phase3_deep_learning.section07_pytorch_fundamentals.exercises import autograd as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("value,expected", [(0.0, 3.0), (1.0, 10.0), (-2.0, 7.0)])
def test_compute_scalar_gradient(value, expected):
    x = torch.tensor(value, requires_grad=True)
    out = m.compute_scalar_gradient(x)
    torch.testing.assert_close(out, torch.tensor(expected))
    assert out.shape == () and not out.requires_grad and x.grad is None


@pytest.mark.parametrize(
    "values,expected", [([0.0, 1.0], [3.0, 5.0]), ([[-1.0, 2.0]], [[1.0, 7.0]]), ([], [])]
)
def test_compute_vector_gradient(values, expected):
    x = torch.tensor(values, requires_grad=True)
    out = m.compute_vector_gradient(x)
    torch.testing.assert_close(out, torch.tensor(expected))
    assert out.shape == x.shape and x.grad is None and not out.requires_grad


@pytest.mark.parametrize("value", [0.0, 1.0, -3.0])
def test_gradient_accumulation_demo(value):
    out = m.gradient_accumulation_demo(torch.tensor(value))
    for name, expected in [
        ("first", 2 * value),
        ("accumulated", 4 * value),
        ("after_zero", 2 * value),
    ]:
        torch.testing.assert_close(out[name], torch.tensor(expected))
        assert not out[name].requires_grad


@pytest.mark.parametrize("shape", [(), (2,), (2, 3)])
def test_detach_tensor(shape):
    x = torch.ones(shape, requires_grad=True)
    y = x * 2
    out = m.detach_tensor(y)
    assert (
        out.shape == shape
        and out.data_ptr() == y.data_ptr()
        and not out.requires_grad
        and out.grad_fn is None
    )
    assert y.requires_grad


@pytest.mark.parametrize("training,width", [(True, 1), (False, 2), (True, 3)])
def test_freeze_parameters(training, width):
    model = nn.Linear(width, 1)
    model.train(training)
    out = m.freeze_parameters(model)
    assert (
        out is model
        and model.training == training
        and all(not p.requires_grad for p in model.parameters())
    )
    x = torch.ones(1, width, requires_grad=True)
    model(x).sum().backward()
    assert x.grad is not None
