import json

import pytest
import torch
from torch import nn

from phase3_deep_learning.section09_deep_learning_engineering.exercises import checkpointing as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("epoch", [0, 1, 7])
def test_save_checkpoint(tmp_path, epoch):
    model = nn.Linear(2, 1)
    opt = torch.optim.Adam(model.parameters(), lr=0.1)
    sch = torch.optim.lr_scheduler.StepLR(opt, 1)
    path = tmp_path / "nested/checkpoint.pt"
    m.save_checkpoint(path, model, opt, sch, epoch, 0.3)
    state = torch.load(path, map_location="cpu", weights_only=True)
    assert state["epoch"] == epoch and state["best_metric"] == 0.3
    assert all(k in state for k in ["model", "optimizer", "scheduler"])
    torch.testing.assert_close(state["model"]["weight"], model.weight)


@pytest.mark.parametrize("epoch", [0, 2, 4])
def test_load_checkpoint(tmp_path, epoch):
    model = nn.Linear(2, 1)
    opt = torch.optim.Adam(model.parameters(), lr=0.1)
    sch = torch.optim.lr_scheduler.StepLR(opt, 1)
    model(torch.ones(1, 2)).sum().backward()
    opt.step()
    sch.step()
    path = tmp_path / "x.pt"
    torch.save(
        {
            "model": model.state_dict(),
            "optimizer": opt.state_dict(),
            "scheduler": sch.state_dict(),
            "epoch": epoch,
            "best_metric": 0.2,
        },
        path,
    )
    restored = nn.Linear(2, 1)
    newopt = torch.optim.Adam(restored.parameters(), lr=0.9)
    newscheduler = torch.optim.lr_scheduler.StepLR(newopt, 1)
    state = m.load_checkpoint(path, restored, newopt, newscheduler)
    torch.testing.assert_close(restored.weight, model.weight)
    assert state["epoch"] == epoch
    assert newopt.param_groups[0]["lr"] == opt.param_groups[0]["lr"] and len(newopt.state) == len(
        opt.state
    )
    assert newscheduler.last_epoch == sch.last_epoch


@pytest.mark.parametrize("loss", [0.0, 0.2, 3.0])
def test_log_experiment(tmp_path, loss):
    path = tmp_path / "logs/history.jsonl"
    m.log_experiment({"epoch": 1, "loss": loss}, path)
    m.log_experiment({"epoch": 2, "loss": loss}, path)
    rows = [json.loads(s) for s in path.read_text().splitlines()]
    assert len(rows) == 2 and rows[1]["epoch"] == 2 and rows[0]["loss"] == loss
