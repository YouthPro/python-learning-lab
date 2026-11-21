"""Real FashionMNIST or explicit offline synthetic smoke mode."""

import argparse
import json
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from phase3_deep_learning.common.checkpoint import load_state
from phase3_deep_learning.common.data import fashion_splits, split_three, synthetic_images
from phase3_deep_learning.common.engine import evaluate_model, probabilities
from phase3_deep_learning.common.experiment import fit_classifier
from phase3_deep_learning.common.models import MLP
from phase3_deep_learning.common.runtime import choose_device, seed_all
from phase3_deep_learning.common.visualization import classification_artifacts


def run(
    output: Path,
    *,
    synthetic: bool = False,
    download: bool = False,
    data_root: Path = Path("datasets/raw/fashion_mnist"),
    epochs: int = 5,
    seed: int = 42,
    hidden_dims: list[int] | None = None,
    device: str = "cpu",
) -> dict:
    """Keep official test data isolated until the best validation epoch is chosen."""
    if synthetic and download:
        raise ValueError("synthetic mode never downloads")
    seed_all(seed)
    target = choose_device(device)
    splits = (
        split_three(synthetic_images(240, classes=10, seed=seed), seed)
        if synthetic
        else fashion_splits(data_root, download=download, seed=seed)
    )
    train, validation, test = splits
    train_loader = DataLoader(
        train, batch_size=64, shuffle=True, generator=torch.Generator().manual_seed(seed)
    )
    val_loader, test_loader = (DataLoader(s, batch_size=64) for s in [validation, test])
    spec = {
        "kind": "mlp",
        "input_shape": [1, 28, 28],
        "hidden_dims": hidden_dims or [128, 64],
        "num_classes": 10,
        "activation": "relu",
        "dropout": 0.0,
    }
    model = MLP(**{k: v for k, v in spec.items() if k != "kind"})
    history = fit_classifier(model, train_loader, val_loader, output, spec, target, epochs=epochs)
    state = load_state(output / "best.pt")
    restored = MLP(**{k: v for k, v in state["model_spec"].items() if k != "kind"}).to(target)
    restored.load_state_dict(state["model"])
    metrics = evaluate_model(restored, test_loader, target)
    classification_artifacts(restored, test_loader, target, output, 10)
    examples, _ = next(iter(test_loader))
    torch.save(probabilities(restored, examples, target), output / "predictions.pt")
    (output / "test_metrics.json").write_text(json.dumps(metrics))
    return {"history": history, "test": metrics}


def main() -> None:
    """Only --download permits FashionMNIST network access."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("outputs/phase3/fashion_mlp"))
    parser.add_argument("--data-root", type=Path, default=Path("datasets/raw/fashion_mnist"))
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--hidden", type=int, nargs="+", default=[128, 64])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    torch.set_num_threads(2)
    print(
        json.dumps(
            run(
                args.output,
                synthetic=args.synthetic,
                download=args.download,
                data_root=args.data_root,
                epochs=args.epochs,
                seed=args.seed,
                hidden_dims=args.hidden,
                device=args.device,
            )["test"]
        )
    )


if __name__ == "__main__":
    main()
