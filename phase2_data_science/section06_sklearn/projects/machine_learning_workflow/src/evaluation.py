"""Evaluate predictions without accessing training or preprocessing state."""

import math

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)


def evaluate(task: str, y_true, y_pred) -> dict:
    if task == "regression":
        mse = float(mean_squared_error(y_true, y_pred))
        return {
            "mae": float(mean_absolute_error(y_true, y_pred)),
            "mse": mse,
            "rmse": math.sqrt(mse),
            "r2": float(r2_score(y_true, y_pred)),
        }
    if task == "classification":
        return {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, zero_division=0)),
            "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
        }
    raise ValueError("unknown task")
