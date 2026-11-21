"""State-dict checkpoints containing tensors and primitive containers only."""

import os
import random
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
import torch


def capture_rng() -> dict[str, Any]:
    """Encode NumPy state without unsafe NumPy objects in the pickle payload."""
    state = np.random.get_state()
    return {
        "python": random.getstate(),
        "numpy_name": state[0],
        "numpy_keys": torch.from_numpy(state[1].astype(np.int64)),
        "numpy_pos": state[2],
        "numpy_gauss": state[3],
        "numpy_cache": state[4],
        "torch": torch.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
    }


def restore_rng(state: dict[str, Any]) -> None:
    """Restore Python/NumPy/Torch random streams on the current machine."""
    random.setstate(state["python"])
    np.random.set_state(
        (
            state["numpy_name"],
            state["numpy_keys"].numpy().astype(np.uint32),
            state["numpy_pos"],
            state["numpy_gauss"],
            state["numpy_cache"],
        )
    )
    torch.set_rng_state(state["torch"].cpu())
    if torch.cuda.is_available() and state["cuda"]:
        torch.cuda.set_rng_state_all([s.cpu() for s in state["cuda"]])


def save_state(path: str | Path, state: dict[str, Any]) -> None:
    """Atomically replace a checkpoint; never serialize an nn.Module object."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    os.close(handle)
    try:
        torch.save(state, temporary)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def load_state(path: str | Path) -> dict[str, Any]:
    """Explicit weights-only CPU loading; use only expected local checkpoints."""
    state = torch.load(Path(path), map_location="cpu", weights_only=True)
    if not isinstance(state, dict) or "model" not in state:
        raise ValueError("checkpoint must be a mapping containing model state")
    return state
