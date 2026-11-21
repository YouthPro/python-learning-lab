"""Strict validation catches malformed YAML without executing objects."""

from copy import deepcopy

import pytest
from training_framework.config import load_config, validate_config


@pytest.mark.parametrize(
    "patch",
    [
        {"training": {"epochs": 0}},
        {"training": {"batch_size": True}},
        {"optimizer": {"lr": float("nan")}},
        {"optimizer": {"lr": float("inf")}},
        {"model": {"input_shape": [1, 0, 16]}},
        {"model": {"name": "transformer"}},
        {"data": {"val_ratio": 1.0}},
        {"training": {"amp": "yes"}},
        {"typo": 4},
    ],
)
def test_reject_invalid(patch):
    with pytest.raises(ValueError):
        validate_config(patch)


def test_defaults_copy_and_no_mutation():
    raw = {"training": {"epochs": 2}}
    copy = deepcopy(raw)
    c = validate_config(raw)
    assert raw == copy and c["model"]["name"] == "mlp" and c["training"]["epochs"] == 2
    c["model"]["input_shape"][0] = 3
    assert validate_config({})["model"]["input_shape"] == [1, 16, 16]


def test_yaml_paths_and_safe_loader(tmp_path):
    folder = tmp_path / "configs"
    folder.mkdir()
    path = folder / "x.yaml"
    path.write_text("run_dir: outputs/demo\ntraining:\n  epochs: 2\n")
    c = load_config(path)
    assert c["run_dir"] == str(tmp_path / "outputs/demo")
    path.write_text('!!python/object/apply:os.system ["echo forbidden"]')
    import yaml

    with pytest.raises(yaml.YAMLError):
        load_config(path)
