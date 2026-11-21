import random

import numpy as np
import pytest
import torch

from phase3_deep_learning.section09_deep_learning_engineering.exercises import reproducibility as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("seed", [0, 7, 42])
def test_seed_everything(seed):
    m.seed_everything(seed)
    first = (random.random(), np.random.random(), torch.rand(3))
    m.seed_everything(seed)
    second = (random.random(), np.random.random(), torch.rand(3))
    assert first[:2] == second[:2]
    torch.testing.assert_close(first[2], second[2])


@pytest.mark.parametrize("updates", [{}, {"epochs": 0}, {"learning_rate": float("nan")}])
def test_validate_config(updates):
    config = dict(epochs=2, batch_size=4, learning_rate=0.01)
    config.update(updates)
    if updates:
        with pytest.raises(ValueError):
            m.validate_config(config)
    else:
        out = m.validate_config(config)
        assert out is not config and out["seed"] == 42 and out["device"] == "cpu"
