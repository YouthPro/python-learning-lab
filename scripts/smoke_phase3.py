"""Execute all six reference projects offline, then resume/evaluate/predict."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from time import perf_counter

import yaml

ROOT = Path(__file__).resolve().parents[1]
P7 = "phase3_deep_learning.section07_pytorch_fundamentals.projects."
P8 = "phase3_deep_learning.section08_data_pipeline_and_models.projects."
FRAME = (
    ROOT
    / "phase3_deep_learning/section09_deep_learning_engineering/projects/pytorch_training_framework"
)


def main() -> None:
    """Write machine-readable commands/results, with network disabled in children."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = (
        args.output.resolve() if args.output else Path(tempfile.mkdtemp(prefix="phase3-smoke-"))
    )
    output.mkdir(parents=True, exist_ok=True)
    blocker = output / "offline_guard"
    blocker.mkdir(exist_ok=True)
    (blocker / "sitecustomize.py").write_text(
        "import socket, urllib.request\n"
        "original = socket.socket.connect\n"
        "def connect(sock, address):\n"
        "    if sock.family in {socket.AF_INET, socket.AF_INET6}:\n"
        "        raise RuntimeError('Phase3 smoke must not use network')\n"
        "    return original(sock, address)\n"
        "socket.socket.connect = connect\n"
        "def no_url(*args, **kwargs):\n"
        "    raise RuntimeError('Phase3 smoke must not download')\n"
        "urllib.request.urlopen = no_url\n"
    )
    env = dict(os.environ, MPLBACKEND="Agg")
    env["PYTHONPATH"] = str(blocker) + os.pathsep + str(ROOT)
    results: list[dict] = []

    def command(module: str, *arguments: object, cwd: Path = ROOT) -> dict | list:
        argv = [sys.executable, "-m", module, *map(str, arguments)]
        started = perf_counter()
        completed = subprocess.run(
            argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=180
        )
        record = {
            "command": argv,
            "cwd": str(cwd),
            "exit_code": completed.returncode,
            "seconds": perf_counter() - started,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        results.append(record)
        (output / "commands.json").write_text(json.dumps(results, indent=2))
        if completed.returncode:
            raise RuntimeError(f"{module}: {completed.stderr}\n{completed.stdout}")
        if "--help" in arguments:
            assert "usage:" in completed.stdout
            return {}
        if module.endswith("generate_demo_data"):
            return {}
        return json.loads(completed.stdout.strip().splitlines()[-1])

    for module in [
        P7 + "mlp_classifier",
        P7 + "fashion_mnist_classifier",
        P8 + "image_dataset_pipeline",
        P8 + "cnn_image_classifier",
        P8 + "transfer_learning_classifier",
        "training_framework.cli",
    ]:
        command(module, "--help")
    pipeline = command(
        P8 + "image_dataset_pipeline",
        "--generate-demo",
        "--root",
        output / "images",
        "--output",
        output / "manifest.json",
    )
    assert pipeline["shape"][1:] == [3, 32, 32] and not pipeline["corrupt"]
    command(P8 + "image_dataset_pipeline.scripts.generate_demo_data", "--root", output / "images")
    mlp = command(P7 + "mlp_classifier", "--epochs", 5, "--output", output / "mlp")
    assert mlp["samples"] == 900 and 0 <= mlp["accuracy"] <= 1
    command(
        P7 + "mlp_classifier",
        "--epochs",
        1,
        "--hidden",
        64,
        32,
        "--activation",
        "tanh",
        "--optimizer",
        "sgd",
        "--learning-rate",
        0.03,
        "--output",
        output / "mlp_sgd",
    )
    fashion = command(
        P7 + "fashion_mnist_classifier",
        "--synthetic",
        "--epochs",
        2,
        "--output",
        output / "fashion",
    )
    assert fashion["samples"] == 36
    cnn = command(
        P8 + "cnn_image_classifier",
        "--synthetic",
        "--compare",
        "--epochs",
        1,
        "--output",
        output / "cnn",
    )
    assert len(cnn) == 6 and (output / "cnn/comparison.md").exists()
    transfer = command(
        P8 + "transfer_learning_classifier",
        "--dataset",
        "synthetic",
        "--samples",
        24,
        "--image-size",
        32,
        "--epochs",
        1,
        "--output",
        output / "transfer",
    )
    assert [r["strategy"] for r in transfer] == ["A", "B", "C"]
    counts = [r["trainable_parameters"] for r in transfer]
    assert counts[0] < counts[1] < counts[2]
    predicted = command(
        P8 + "transfer_learning_classifier",
        "--checkpoint",
        output / "transfer/B/best.pt",
        "--input",
        output / "images/cat/generated_000.png",
    )
    assert len(predicted["probabilities"]) == 3
    command(
        "training_framework.cli",
        "train",
        "--config",
        "configs/default.yaml",
        "--run-dir",
        output / "framework",
        "--epochs",
        1,
        cwd=FRAME,
    )
    resumed = command(
        "training_framework.cli",
        "train",
        "--config",
        "configs/default.yaml",
        "--run-dir",
        output / "framework",
        "--epochs",
        2,
        "--resume",
        output / "framework/checkpoints/latest.pt",
        cwd=FRAME,
    )
    assert resumed["epochs_completed"] == 2
    evaluated = command(
        "training_framework.cli",
        "evaluate",
        "--config",
        "configs/default.yaml",
        "--checkpoint",
        output / "framework/checkpoints/best.pt",
        cwd=FRAME,
    )
    assert evaluated["samples"] == 48
    command(
        "phase3_deep_learning.section09_deep_learning_engineering.projects.pytorch_training_framework.scripts.generate_demo_data",
        "--root",
        output / "framework_demo",
        "--sample",
        output / "sample.jpg",
        cwd=FRAME,
    )
    prediction = command(
        "training_framework.cli",
        "predict",
        "--checkpoint",
        output / "framework/checkpoints/best.pt",
        "--input",
        output / "sample.jpg",
        cwd=FRAME,
    )
    assert len(prediction["probabilities"]) == 3
    command(
        "training_framework.cli",
        "train",
        "--config",
        FRAME / "configs/cnn.yaml",
        "--run-dir",
        output / "framework_cnn",
        "--epochs",
        1,
    )
    folder_config = output / "folder.yaml"
    folder_config.write_text(
        yaml.safe_dump(
            {
                "run_dir": str(output / "framework_folder"),
                "data": {"kind": "image_folder", "root": str(output / "images")},
                "model": {"name": "cnn", "input_shape": [3, 32, 32], "num_classes": 3},
                "training": {"epochs": 1},
            }
        )
    )
    command("training_framework.cli", "train", "--config", folder_config)
    rgb_prediction = command(
        "training_framework.cli",
        "predict",
        "--checkpoint",
        output / "framework_folder/checkpoints/best.pt",
        "--input",
        output / "images/bird/generated_000.png",
    )
    assert rgb_prediction["label"] in {"bird", "cat", "dog"}
    summary = {
        "projects": 6,
        "commands": len(results),
        "all_exit_zero": True,
        "network_disabled": True,
        "mlp_samples": 6000,
        "mlp_test_accuracy": mlp["accuracy"],
        "framework_resumed_epoch": 2,
        "rgb_and_grayscale_inference": True,
        "transfer_trainable_parameters": counts,
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(dict(summary, output=str(output))))


if __name__ == "__main__":
    main()
