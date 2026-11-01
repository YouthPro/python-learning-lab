"""Input validation and optional offline sklearn classification generation."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

HOUSE_FEATURES = [
    "area",
    "bedrooms",
    "bathrooms",
    "house_age",
    "distance_to_city",
    "location_score",
]


def load_dataset(
    task: str, path: str | Path | None, random_state: int = 42, n_samples: int = 500
) -> tuple[pd.DataFrame, pd.Series]:
    if task not in {"regression", "classification"}:
        raise ValueError("unknown task")
    if task == "classification" and path is None:
        X, y = make_classification(
            n_samples=n_samples,
            n_features=10,
            n_informative=6,
            n_redundant=2,
            random_state=random_state,
        )
        return pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)]), pd.Series(
            y, name="target"
        )
    if path is None:
        raise ValueError("regression input CSV is required")
    df = pd.read_csv(path)
    target = "price" if task == "regression" else "target"
    features = HOUSE_FEATURES if task == "regression" else [c for c in df if c != target]
    missing = set([*features, target]) - set(df)
    if missing or not features:
        raise ValueError(f"missing schema columns {sorted(missing)}")
    X = df[features].apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(df[target], errors="coerce")
    if len(X) == 0 or not np.isfinite(y).all() or np.isinf(X.to_numpy()).any():
        raise ValueError(
            "nonempty data with finite targets and finite or missing features required"
        )
    if task == "classification" and set(y.unique()) != {0, 1}:
        raise ValueError("classification requires both binary labels 0 and 1")
    return X, y
