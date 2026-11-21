"""Engineering learner TODOs; no full exercise solutions."""

from typing import Any


def seed_everything(seed: int) -> None:
    """01. Set Random Seed. Seed Python random, NumPy and Torch (and CUDA if available); same-environment reproducibility, not across platforms.
    Input Shape -> Output Shape: seed scalar -> None
    Expected dtype: Python int
    Grad / computation graph: no graph
    Hint: Seed all RNGs; distinguish deterministic algorithms from seeds."""
    # TODO
    raise NotImplementedError


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    """02. Experiment Config. Minimal flat exercise config: required epochs,batch_size positive integers (not bool),learning_rate finite positive; defaults seed=42/device=cpu, supported device cpu/cuda/mps/auto. Return new dict; invalid raises ValueError.
    Input Shape -> Output Shape: mapping -> validated mapping
    Expected dtype: primitive scalars
    Grad / computation graph: no graph
    Hint: Read YAML with safe_load outside this function; reject nan and strings as numeric values."""
    # TODO
    raise NotImplementedError
