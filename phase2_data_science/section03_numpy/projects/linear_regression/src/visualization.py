"""Save training loss and target/prediction comparison without show()."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def save_plots(history, y, predictions, output):
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(history, label="MSE")
    axes[0].set(title="Gradient descent", xlabel="Epoch", ylabel="MSE")
    axes[0].legend()
    axes[1].scatter(y, predictions, s=10, label="Predictions")
    axes[1].set(title="Predicted vs actual", xlabel="Actual", ylabel="Predicted")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(root / "training.png", dpi=150)
    plt.close(fig)
