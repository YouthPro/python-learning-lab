"""Estimator construction is independent of evaluation."""

from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC


def build_models(task: str, random_state: int = 42) -> dict:
    if task == "regression":
        return {
            "linear": LinearRegression(),
            "random_forest": RandomForestRegressor(random_state=random_state, n_jobs=1),
            "gradient_boosting": GradientBoostingRegressor(random_state=random_state),
        }
    if task == "classification":
        return {
            "logistic": LogisticRegression(max_iter=2000, random_state=random_state),
            "random_forest": RandomForestClassifier(random_state=random_state, n_jobs=1),
            "svm": SVC(random_state=random_state),
        }
    raise ValueError("task must be regression or classification")
