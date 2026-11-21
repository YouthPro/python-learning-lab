"""Safe YAML and strict, typed configuration validation."""

import math
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

DEFAULTS = {
    "seed": 42,
    "device": "cpu",
    "threads": 2,
    "run_dir": ".",
    "data": {"kind": "synthetic", "samples": 240, "val_ratio": 0.2, "root": None, "num_workers": 0},
    "model": {
        "name": "mlp",
        "input_shape": [1, 16, 16],
        "num_classes": 3,
        "hidden_dims": [32],
        "activation": "relu",
        "dropout": 0.1,
        "depth": 2,
    },
    "training": {
        "epochs": 3,
        "batch_size": 32,
        "gradient_accumulation": 1,
        "max_grad_norm": 1.0,
        "amp": False,
    },
    "optimizer": {"name": "adam", "lr": 0.01, "momentum": 0.9, "weight_decay": 0.0},
    "scheduler": {"name": "step", "step_size": 2, "gamma": 0.5, "patience": 2},
    "early_stopping": {"patience": 8, "min_delta": 0.0},
}


def _merge(base: dict, changes: dict, prefix: str = "") -> dict:
    """Reject typos rather than silently ignoring unknown hyperparameters."""
    if not isinstance(changes, dict):
        raise ValueError(f"{prefix or 'config'} must be a mapping")
    for key, value in changes.items():
        if key not in base:
            raise ValueError(f"unknown configuration key: {prefix}{key}")
        if isinstance(base[key], dict):
            _merge(base[key], value, prefix + key + ".")
        else:
            base[key] = value
    return base


def _integer(value: Any, name: str, minimum: int = 1) -> None:
    """Bool is not accepted as an integer hyperparameter."""
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _number(value: Any, name: str, minimum: float = 0, strict: bool = False) -> None:
    """Reject strings, bool, NaN and infinity."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be finite and numeric")
    if value < minimum or (strict and value == minimum):
        raise ValueError(f"{name} out of range")


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    """Merge documented defaults into a copy and validate every supported field."""
    c = _merge(deepcopy(DEFAULTS), deepcopy(config))
    for key in ["seed", "threads"]:
        _integer(c[key], key, 0 if key == "seed" else 1)
    if not isinstance(c["device"], str) or (
        c["device"] not in {"auto", "cpu", "cuda", "mps"} and not c["device"].startswith("cuda:")
    ):
        raise ValueError("unsupported device")
    if not isinstance(c["run_dir"], str) or not c["run_dir"]:
        raise ValueError("run_dir must be a nonempty string")
    d, m, t, o, s, e = (
        c[k] for k in ["data", "model", "training", "optimizer", "scheduler", "early_stopping"]
    )
    if d["kind"] not in {"synthetic", "image_folder"}:
        raise ValueError("data.kind must be synthetic or image_folder")
    _integer(d["samples"], "samples", 8)
    _integer(d["num_workers"], "num_workers", 0)
    _number(d["val_ratio"], "val_ratio", strict=True)
    if d["val_ratio"] >= 1:
        raise ValueError("val_ratio must be <1")
    if d["root"] is not None and not isinstance(d["root"], str):
        raise ValueError("data.root must be a path string")
    if d["kind"] == "image_folder" and not d["root"]:
        raise ValueError("image_folder needs data.root")
    if m["name"] not in {"mlp", "cnn"}:
        raise ValueError("unknown model")
    shape = m["input_shape"]
    if not isinstance(shape, list) or len(shape) != 3:
        raise ValueError("input_shape must be [C,H,W]")
    for v in shape:
        _integer(v, "input_shape")
    if shape[0] not in {1, 3} or shape[1] != shape[2] or shape[1] < 8:
        raise ValueError("square images >=8, C=1 or 3 required")
    if d["kind"] == "image_folder" and shape[0] != 3:
        raise ValueError("image_folder supplies RGB images")
    _integer(m["num_classes"], "num_classes", 2)
    if d["kind"] == "synthetic" and m["num_classes"] > shape[1]:
        raise ValueError("synthetic classes must fit image width")
    if not isinstance(m["hidden_dims"], list):
        raise ValueError("hidden_dims must be a list")
    for v in m["hidden_dims"]:
        _integer(v, "hidden_dims")
    _integer(m["depth"], "depth")
    if m["depth"] > 3 or shape[1] < 2 ** m["depth"]:
        raise ValueError("CNN depth/size mismatch")
    if m["activation"] not in {"relu", "tanh", "gelu"}:
        raise ValueError("unknown activation")
    _number(m["dropout"], "dropout")
    if m["dropout"] >= 1:
        raise ValueError("dropout must be <1")
    for key in ["epochs", "batch_size", "gradient_accumulation"]:
        _integer(t[key], key)
    if t["max_grad_norm"] is not None:
        _number(t["max_grad_norm"], "max_grad_norm", strict=True)
    if type(t["amp"]) is not bool:
        raise ValueError("amp must be bool")
    if o["name"] not in {"adam", "sgd"}:
        raise ValueError("unknown optimizer")
    _number(o["lr"], "lr", strict=True)
    _number(o["weight_decay"], "weight_decay")
    _number(o["momentum"], "momentum")
    if s["name"] not in {"step", "plateau", "none"}:
        raise ValueError("unknown scheduler")
    _integer(s["step_size"], "step_size")
    _integer(s["patience"], "scheduler.patience", 0)
    _number(s["gamma"], "gamma", strict=True)
    if not s["gamma"] < 1:
        raise ValueError("gamma must be <1")
    _integer(e["patience"], "early_stopping.patience")
    _number(e["min_delta"], "min_delta")
    return c


def load_config(path: str | Path) -> dict[str, Any]:
    """Resolve relative run/data paths against the project's config parent."""
    path = Path(path).resolve()
    with path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    config = validate_config(raw)
    base = path.parent.parent
    for parent, key in [(config, "run_dir"), (config["data"], "root")]:
        if parent[key] is not None:
            value = Path(parent[key])
            parent[key] = str(value if value.is_absolute() else (base / value).resolve())
    return config
