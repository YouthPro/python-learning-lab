"""Train A/B/C ResNet18 comparisons or infer one image without downloading weights."""

import argparse
import csv
import json
from pathlib import Path
from time import perf_counter

import torch
from PIL import Image
from torch.utils.data import DataLoader

from phase3_deep_learning.common.checkpoint import load_state
from phase3_deep_learning.common.engine import evaluate_model, probabilities
from phase3_deep_learning.common.experiment import fit_classifier
from phase3_deep_learning.common.runtime import choose_device, seed_all
from phase3_deep_learning.section08_data_pipeline_and_models.projects.image_dataset_pipeline.src.dataset import (
    image_transforms,
)

from .data import datasets
from .models import make_resnet, set_strategy


def run(
    output: Path,
    *,
    dataset: str = "synthetic",
    root: Path = Path("datasets/raw/transfer"),
    download_data: bool = False,
    pretrained: bool = False,
    epochs: int = 1,
    samples: int = 96,
    image_size: int = 64,
    seed: int = 42,
    device: str = "cpu",
    strategies: tuple[str, ...] = ("A", "B", "C"),
) -> list[dict]:
    """Compare validation accuracy/time/trainable parameters from equal initial weights.

    Actual pretrained experiments use 224 RGB and ImageNet normalization. The
    offline random-weight mode is only an engineering smoke, not transfer benefit.
    """
    image_size = 224 if pretrained else image_size
    target = choose_device(device)
    rows = []
    for strategy in strategies:
        seed_all(seed)
        train, validation, classes = datasets(
            dataset, root, download=download_data, seed=seed, samples=samples, image_size=image_size
        )
        model = set_strategy(make_resnet(len(classes), pretrained=pretrained), strategy)
        # A training ResNet BN cannot estimate variance from a last singleton
        # at 1x1 spatial resolution. Only that singleton is omitted.
        train_loader = DataLoader(
            train,
            batch_size=min(8, len(train)),
            shuffle=True,
            drop_last=len(train) > 8 and len(train) % 8 == 1,
            generator=torch.Generator().manual_seed(seed),
        )
        val_loader = DataLoader(validation, batch_size=8)
        spec = {
            "kind": "resnet18",
            "num_classes": len(classes),
            "image_size": image_size,
            "classes": classes,
            "strategy": strategy,
            "pretrained": pretrained,
        }
        started = perf_counter()
        fit_classifier(
            model,
            train_loader,
            val_loader,
            output / strategy,
            spec,
            target,
            epochs=epochs,
            learning_rate=0.001 if strategy == "A" else 0.0001,
        )
        elapsed = perf_counter() - started
        metrics = evaluate_model(model, val_loader, target)
        rows.append(
            {
                "strategy": strategy,
                "val_accuracy": metrics["accuracy"],
                "val_loss": metrics["loss"],
                "training_seconds": elapsed,
                "trainable_parameters": sum(
                    p.numel() for p in model.parameters() if p.requires_grad
                ),
                "total_parameters": sum(p.numel() for p in model.parameters()),
                "pretrained": pretrained,
                "dataset": dataset,
                "learning_rate": 0.001 if strategy == "A" else 0.0001,
            }
        )
    output.mkdir(parents=True, exist_ok=True)
    with (output / "comparison.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output / "comparison.json").write_text(json.dumps(rows, indent=2))
    return rows


def infer(checkpoint: Path, image: Path, device: str = "cpu") -> dict:
    """Reconstruct random-weight architecture then load the entire saved state."""
    target = choose_device(device)
    state = load_state(checkpoint)
    spec = state["model_spec"]
    model = make_resnet(spec["num_classes"], pretrained=False).to(target)
    model.load_state_dict(state["model"])
    with Image.open(image) as source:
        inputs = image_transforms(spec["image_size"], False)(source).unsqueeze(0)
    probs = probabilities(model, inputs, target)[0]
    index = int(probs.argmax())
    return {"index": index, "label": spec["classes"][index], "probabilities": probs.tolist()}


def main() -> None:
    """Downloads require --download-data and/or --pretrained, independently."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("outputs/phase3/transfer"))
    parser.add_argument(
        "--dataset",
        choices=["synthetic", "fashion_mnist", "cifar10", "folder"],
        default="synthetic",
    )
    parser.add_argument("--root", type=Path, default=Path("datasets/raw/transfer"))
    parser.add_argument("--download-data", action="store_true")
    parser.add_argument("--pretrained", action="store_true")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--samples", type=int, default=96)
    parser.add_argument("--image-size", type=int, default=64)
    parser.add_argument("--strategies", nargs="+", choices=["A", "B", "C"], default=["A", "B", "C"])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--input", type=Path)
    args = vars(parser.parse_args())
    checkpoint, image = args.pop("checkpoint"), args.pop("input")
    torch.set_num_threads(2)
    if checkpoint or image:
        if not checkpoint or not image:
            parser.error("--checkpoint and --input must be used together")
        print(json.dumps(infer(checkpoint, image, args["device"])))
    else:
        output = args.pop("output")
        print(json.dumps(run(output, **args)))


if __name__ == "__main__":
    main()
