"""EDA artifacts describe the training split only."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


def save_eda(X, y, output: str | Path) -> None:
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    X.describe().to_csv(root / "feature_statistics.csv")
    X.isna().sum().rename("missing_count").to_csv(root / "missing_values.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    try:
        axes[0].hist(y, bins=20)
        axes[0].set(title="Training target distribution", xlabel="Target", ylabel="Count")
        image = axes[1].imshow(X.corr().to_numpy(), vmin=-1, vmax=1, cmap="coolwarm")
        axes[1].set(title="Training feature correlation", xlabel="Feature", ylabel="Feature")
        axes[1].set_xticks(range(X.shape[1]), X.columns, rotation=90)
        axes[1].set_yticks(range(X.shape[1]), X.columns)
        fig.colorbar(image, ax=axes[1])
        fig.tight_layout()
        fig.savefig(root / "eda.png", dpi=150)
    finally:
        plt.close(fig)


def save_evaluation(task: str, y_true, y_pred, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    try:
        if task == "classification":
            ConfusionMatrixDisplay.from_predictions(y_true, y_pred, labels=[0, 1], ax=ax)
            ax.set_title("Held-out confusion matrix")
        else:
            ax.scatter(y_true, y_pred, s=15, label="Predictions")
            ax.set(title="Held-out predictions", xlabel="Actual price", ylabel="Predicted price")
            ax.legend()
        fig.tight_layout()
        fig.savefig(path, dpi=150)
    finally:
        plt.close(fig)
