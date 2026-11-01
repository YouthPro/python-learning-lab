import argparse
from pathlib import Path

import numpy as np

from .src.linear_regression import LinearRegression
from .src.visualization import save_plots


def main(argv=None):
    parser = argparse.ArgumentParser(description="Linear regression from scratch")
    parser.add_argument("--input", default="datasets/generated/regression.npz")
    parser.add_argument("--output", default="datasets/processed/numpy_regression")
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args(argv)
    try:
        with np.load(args.input, allow_pickle=False) as dataset:
            X, y = dataset["X"], dataset["y"]
        model = LinearRegression(
            epochs=args.epochs, batch_size=args.batch_size, random_state=args.random_state
        ).fit(X, y)
        predictions = model.predict(X)
        root = Path(args.output)
        root.mkdir(parents=True, exist_ok=True)
        np.savez(root / "parameters.npz", weights=model.weights_, bias=model.bias_)
        np.savetxt(
            root / "loss.csv",
            np.c_[np.arange(len(model.loss_history_)), model.loss_history_],
            delimiter=",",
            header="epoch,mse",
            comments="",
        )
        np.savetxt(
            root / "predictions.csv",
            np.c_[y, predictions],
            delimiter=",",
            header="actual,prediction",
            comments="",
        )
        save_plots(model.loss_history_, y, predictions, root)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"{exc}\n")
    print(f"MSE={model.loss_history_[-1]:.6f}")


if __name__ == "__main__":
    main()
