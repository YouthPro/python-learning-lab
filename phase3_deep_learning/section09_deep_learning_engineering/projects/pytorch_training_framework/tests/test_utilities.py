"""Uneven sample weighting, remainder accumulation, stopping, optimizers and devices."""

import random

import numpy as np
import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from training_framework.config import validate_config
from training_framework.engine.optim import build_optimizer, build_scheduler
from training_framework.utils.early_stopping import EarlyStopping

from phase3_deep_learning.common.checkpoint import capture_rng, load_state, restore_rng, save_state
from phase3_deep_learning.common.engine import evaluate_model, train_epoch
from phase3_deep_learning.common.runtime import choose_device, seed_all


def test_sample_weighted_eval_and_mode_restoration():
    inputs = torch.tensor([[4.0, 0.0], [0.0, 3.0], [1.0, 1.0], [0.0, 2.0], [2.0, 0.0]])
    labels = torch.tensor([0, 0, 1, 1, 0])
    model = nn.Identity()
    model.train()
    result = evaluate_model(
        model, DataLoader(TensorDataset(inputs, labels), batch_size=2), torch.device("cpu")
    )
    expected = nn.functional.cross_entropy(inputs, labels).item()
    assert result["loss"] == pytest.approx(expected) and result["samples"] == 5
    assert result["accuracy"] == 0.6 and model.training


def test_remainder_accumulation_matches_large_batch():
    torch.manual_seed(6)
    a = nn.Linear(2, 2)
    b = nn.Linear(2, 2)
    b.load_state_dict(a.state_dict())
    data = TensorDataset(torch.randn(5, 2), torch.tensor([0, 1, 0, 1, 1]))
    for model, batch, accumulation in [(a, 2, 3), (b, 5, 1)]:
        train_epoch(
            model,
            DataLoader(data, batch_size=batch),
            torch.optim.SGD(model.parameters(), lr=0.1),
            torch.device("cpu"),
            accumulation_steps=accumulation,
        )
    for left, right in zip(a.parameters(), b.parameters(), strict=True):
        torch.testing.assert_close(left, right, rtol=1e-6, atol=1e-7)


def test_early_stopping_and_rng_checkpoint(tmp_path):
    stopper = EarlyStopping(2)
    assert not stopper.update(1)
    assert not stopper.update(2)
    assert stopper.update(2)
    assert not stopper.update(0.5) and stopper.bad_epochs == 0
    seed_all(123)
    state = capture_rng()
    expected = (random.random(), np.random.random(), torch.rand(2))
    save_state(tmp_path / "rng.pt", {"model": {}, "rng": state})
    restore_rng(load_state(tmp_path / "rng.pt")["rng"])
    assert random.random() == expected[0] and np.random.random() == expected[1]
    torch.testing.assert_close(torch.rand(2), expected[2])


@pytest.mark.parametrize("scheduler", ["step", "plateau", "none"])
def test_optimizer_scheduler_factories(scheduler):
    c = validate_config(
        {"optimizer": {"name": "sgd"}, "scheduler": {"name": scheduler, "step_size": 1}}
    )
    model = nn.Linear(2, 2)
    opt = build_optimizer(model, c["optimizer"])
    sch = build_scheduler(opt, c["scheduler"])
    if sch is None:
        assert scheduler == "none"
    elif scheduler == "plateau":
        sch.step(1.0)
        assert sch.last_epoch == 1
    else:
        opt.step()
        sch.step()
        assert opt.param_groups[0]["lr"] == pytest.approx(0.005)


def test_device_fallback_and_unavailable_request(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    monkeypatch.setattr(torch.backends.mps, "is_available", lambda: False)
    assert choose_device("auto") == torch.device("cpu")
    with pytest.raises(ValueError):
        choose_device("cuda")
    with pytest.raises(ValueError):
        choose_device("mps")
