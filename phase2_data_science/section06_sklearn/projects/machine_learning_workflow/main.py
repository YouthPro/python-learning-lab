import argparse
import json
from pathlib import Path

import yaml

from .src.pipeline import predict_file, train_workflow

PROJECT = Path(__file__).resolve().parent


def main(argv=None):
    p = argparse.ArgumentParser(description="Regression and classification ML workflow")
    p.add_argument("--config", type=Path, default=PROJECT / "configs/config.yaml")
    p.add_argument("--task", choices=["regression", "classification", "all"], default="all")
    p.add_argument("--output", type=Path, default=PROJECT)
    p.add_argument("--random-state", type=int)
    p.add_argument("--predict-model", type=Path)
    p.add_argument("--input", type=Path, help="new CSV for prediction mode")
    p.add_argument(
        "--predictions", type=Path, default=Path("datasets/processed/ml_predictions.csv")
    )
    args = p.parse_args(argv)
    try:
        if args.predict_model:
            if not args.input:
                p.error("--input is required with --predict-model")
            result = predict_file(args.predict_model, args.input, args.predictions)
            print(f"predictions={len(result)}")
            return
        config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("config must be a YAML mapping")
        if args.random_state is not None:
            config["random_state"] = args.random_state
        for task in ["regression", "classification"] if args.task == "all" else [args.task]:
            report = train_workflow(config, task, args.output)
            print(
                json.dumps(
                    {
                        "task": task,
                        "selected_model": report["selected_model"],
                        "metrics": report["metrics"],
                    }
                )
            )
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        p.exit(2, f"{exc}\n")


if __name__ == "__main__":
    main()
