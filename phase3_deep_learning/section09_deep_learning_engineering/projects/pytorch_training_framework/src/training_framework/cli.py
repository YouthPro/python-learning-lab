"""python -m training_framework.cli train/evaluate/predict."""

import argparse
import json
from pathlib import Path

from phase3_deep_learning.common.runtime import choose_device

from .config import load_config
from .datasets import build_data
from .engine.evaluator import evaluate, load_model
from .engine.predictor import predict_image
from .engine.trainer import Trainer


def main() -> None:
    """CPU defaults; checkpoint inference does not require an external config."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    train = commands.add_parser("train")
    train.add_argument("--config", type=Path, required=True)
    train.add_argument("--resume", type=Path)
    train.add_argument("--epochs", type=int)
    train.add_argument("--run-dir", type=Path)
    train.add_argument("--device")
    val = commands.add_parser("evaluate")
    val.add_argument("--config", type=Path, required=True)
    val.add_argument("--checkpoint", type=Path, required=True)
    val.add_argument("--device")
    pred = commands.add_parser("predict")
    pred.add_argument("--checkpoint", type=Path, required=True)
    pred.add_argument("--input", type=Path, required=True)
    pred.add_argument("--device", default="cpu")
    args = parser.parse_args()
    if args.command == "predict":
        print(json.dumps(predict_image(args.checkpoint, args.input, args.device)))
        return
    config = load_config(args.config)
    if args.device:
        config["device"] = args.device
    if args.command == "train":
        if args.epochs is not None:
            config["training"]["epochs"] = args.epochs
        if args.run_dir is not None:
            config["run_dir"] = str(args.run_dir.resolve())
        history = Trainer(config).fit(args.resume)
        print(
            json.dumps(
                {
                    "epochs_completed": history[-1]["epoch"] if history else 0,
                    "run_dir": config["run_dir"],
                }
            )
        )
    else:
        device = choose_device(config["device"])
        data = build_data(config, persist_split=False)
        model, state = load_model(args.checkpoint, device)
        if data.fingerprint != state["fingerprint"] or config["model"] != state["model_spec"]:
            raise ValueError("evaluation dataset/model differs from checkpoint")
        print(json.dumps(evaluate(model, data.validation, device)))


if __name__ == "__main__":
    main()
