import pytest
import torch
from torch import nn

from phase3_deep_learning.section09_deep_learning_engineering.exercises import (
    training_utilities as m,
)

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("n", [1, 2, 5])
def test_AverageMeter(n):
    meter = m.AverageMeter()
    meter.update(2, n)
    meter.update(8, 1)
    assert (
        meter.count == n + 1
        and meter.sum == 2 * n + 8
        and meter.avg == pytest.approx((2 * n + 8) / (n + 1))
    )
    meter.reset()
    assert meter.avg == meter.sum == meter.count == 0


@pytest.mark.parametrize(
    "losses,expected",
    [
        ([1, 1, 1], [False, False, True]),
        ([3, 2, 1], [False, False, False]),
        ([1, 2, 0.5], [False, False, False]),
    ],
)
def test_EarlyStopping(losses, expected):
    stop = m.EarlyStopping(patience=2)
    assert [stop.update(v) for v in losses] == expected


@pytest.mark.parametrize("limit", [0.5, 1.0, 2.0])
def test_clip_gradients(limit):
    model = nn.Linear(2, 1, bias=False)
    model.weight.grad = torch.tensor([[3.0, 4.0]])
    assert m.clip_gradients(model, limit) == pytest.approx(5.0)
    assert float(model.weight.grad.norm()) <= limit + 1e-5


@pytest.mark.parametrize("name", ["adam", "sgd", "other"])
def test_build_optimizer(name):
    model = nn.Sequential(nn.Linear(2, 3), nn.Linear(3, 1))
    model[0].requires_grad_(False)
    if name == "other":
        with pytest.raises(ValueError):
            m.build_optimizer(model, {"name": name, "lr": 0.1})
    else:
        opt = m.build_optimizer(model, {"name": name, "lr": 0.1})
        assert {id(p) for g in opt.param_groups for p in g["params"]} == {
            id(p) for p in model[1].parameters()
        }


@pytest.mark.parametrize("name", ["step", "plateau", "none"])
def test_build_scheduler(name):
    model = nn.Linear(1, 1)
    opt = torch.optim.SGD(model.parameters(), lr=0.1)
    scheduler = m.build_scheduler(
        opt, {"name": name, "step_size": 1, "gamma": 0.5, "factor": 0.5, "patience": 0}
    )
    if name == "none":
        assert scheduler is None
    elif name == "step":
        opt.step()
        scheduler.step()
        assert opt.param_groups[0]["lr"] == pytest.approx(0.05)
    else:
        scheduler.step(1)
        scheduler.step(2)
        assert opt.param_groups[0]["lr"] == pytest.approx(0.05)
