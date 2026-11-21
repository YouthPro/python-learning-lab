import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from phase3_deep_learning.section07_pytorch_fundamentals.exercises import neural_network as m

pytestmark = pytest.mark.exercise


def loader(n=7):
    return DataLoader(
        TensorDataset(torch.ones(n, 2), torch.zeros(n, dtype=torch.long)), batch_size=3
    )


@pytest.mark.parametrize("hidden", [[], [4], [4, 3]])
def test_build_mlp(hidden):
    model = m.build_mlp(2, hidden, 3)
    out = model(torch.ones(5, 2))
    assert isinstance(model, nn.Module) and out.shape == (5, 3) and out.requires_grad
    assert not isinstance(list(model.modules())[-1], nn.Softmax)


@pytest.mark.parametrize("freeze,width,expected", [(False, 2, 9), (True, 3, 12), (False, 1, 6)])
def test_count_parameters(freeze, width, expected):
    model = nn.Linear(width, 3)
    if freeze:
        model.requires_grad_(False)
    assert m.count_parameters(model) == expected


@pytest.mark.parametrize("n", [1, 7, 9])
def test_train_one_epoch(n):
    torch.manual_seed(3)
    model = nn.Linear(2, 2)
    model.eval()
    before = model.weight.detach().clone()
    out = m.train_one_epoch(
        model, loader(n), torch.optim.SGD(model.parameters(), lr=0.1), nn.CrossEntropyLoss(), "cpu"
    )
    assert out["samples"] == n and 0 <= out["accuracy"] <= 1 and out["loss"] > 0
    assert model.training and not torch.equal(before, model.weight)


@pytest.mark.parametrize("training,n", [(True, 1), (False, 7), (True, 9)])
def test_evaluate(training, n):
    class Guard(nn.Linear):
        def forward(self, x):
            assert not torch.is_grad_enabled() and not self.training
            return super().forward(x)

    model = Guard(2, 2)
    model.train(training)
    inputs = torch.arange(n * 2, dtype=torch.float32).reshape(n, 2) / 5
    targets = torch.arange(n) % 2
    data = DataLoader(TensorDataset(inputs, targets), batch_size=3)
    out = m.evaluate(model, data, nn.CrossEntropyLoss(), "cpu")
    assert (
        out["samples"] == n
        and model.training == training
        and all(p.grad is None for p in model.parameters())
    )
    with torch.no_grad():
        expected = nn.functional.cross_entropy(
            nn.functional.linear(inputs, model.weight, model.bias), targets
        )
    assert out["loss"] == pytest.approx(expected.item())


@pytest.mark.parametrize("n", [1, 7, 9])
def test_predict_proba(n):
    model = nn.Linear(2, 3)
    model.train()
    out = m.predict_proba(model, loader(n), "cpu")
    assert (
        out.shape == (n, 3)
        and out.device.type == "cpu"
        and not out.requires_grad
        and model.training
    )
    torch.testing.assert_close(out.sum(1), torch.ones(n))
    torch.testing.assert_close(out, model(torch.ones(n, 2)).softmax(1).detach())
