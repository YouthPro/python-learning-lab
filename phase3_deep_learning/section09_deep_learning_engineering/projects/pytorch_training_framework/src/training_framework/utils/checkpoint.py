"""Explicit safe checkpoint APIs, RNG serialization and schema validation."""

from pathlib import Path

from phase3_deep_learning.common.checkpoint import capture_rng, load_state, restore_rng, save_state


def load_checkpoint(path: str | Path) -> dict:
    """Load weights-only on CPU and reject unsupported/missing training metadata."""
    state = load_state(path)
    required = {
        "schema_version",
        "model",
        "optimizer",
        "scheduler",
        "epoch",
        "config",
        "model_spec",
        "history",
        "best_metric",
        "best_epoch",
        "early_stopping",
        "rng",
        "train_generator",
        "val_generator",
        "fingerprint",
        "classes",
        "preprocess",
        "scaler",
    }
    if not required <= state.keys() or state["schema_version"] != 1:
        raise ValueError("unsupported or incomplete training checkpoint")
    return state


__all__ = ["load_checkpoint", "save_state", "capture_rng", "restore_rng"]
