"""NumPy-only regression math and optimization; visualization imports are separate."""

import numpy as np


def as_matrix(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X[:, None]
    if X.ndim != 2 or not np.isfinite(X).all():
        raise ValueError("X must be a finite matrix")
    return X


def mse_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    a, b = np.asarray(y_true), np.asarray(y_pred)
    if a.shape != b.shape or a.size == 0:
        raise ValueError("matching nonempty target shapes required")
    return float(np.mean((a - b) ** 2))


def gradients(
    X: np.ndarray, y: np.ndarray, weights: np.ndarray, bias: float
) -> tuple[np.ndarray, float]:
    error = X @ weights + bias - y
    return 2 / X.shape[0] * (X.T @ error), float(2 * np.mean(error))


class LinearRegression:
    def __init__(
        self,
        learning_rate: float = 0.05,
        epochs: int = 300,
        batch_size: int | None = None,
        random_state: int = 42,
    ):
        if (
            learning_rate <= 0
            or not np.isfinite(learning_rate)
            or epochs <= 0
            or (batch_size is not None and batch_size <= 0)
        ):
            raise ValueError("positive learning rate, epochs and batch size required")
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.random_state = random_state

    def fit(self, X: np.ndarray, y: np.ndarray):
        X = as_matrix(X)
        y = np.asarray(y, dtype=float)
        if y.shape != (len(X),) or len(X) == 0 or not np.isfinite(y).all():
            raise ValueError("finite nonempty y of shape (N,) required")
        self.weights_ = np.zeros(X.shape[1])
        self.bias_ = 0.0
        self.loss_history_ = [mse_loss(y, X @ self.weights_ + self.bias_)]
        rng = np.random.default_rng(self.random_state)
        size = self.batch_size or len(X)
        for _ in range(self.epochs):
            order = rng.permutation(len(X)) if self.batch_size else np.arange(len(X))
            for start in range(0, len(X), size):
                indices = order[start : start + size]
                dw, db = gradients(X[indices], y[indices], self.weights_, self.bias_)
                self.weights_ -= self.learning_rate * dw
                self.bias_ -= self.learning_rate * db
            loss = mse_loss(y, self.predict(X))
            if not np.isfinite(loss):
                raise ValueError("optimization diverged; reduce learning_rate")
            self.loss_history_.append(loss)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not hasattr(self, "weights_"):
            raise ValueError("fit the model first")
        X = as_matrix(X)
        if X.shape[1] != len(self.weights_):
            raise ValueError("feature count mismatch")
        return X @ self.weights_ + self.bias_
