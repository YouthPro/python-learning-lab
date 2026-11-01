import numpy as np
import pytest

from phase2_data_science.section03_numpy.projects.linear_regression.src.linear_regression import (
    LinearRegression,
    gradients,
    mse_loss,
)
from phase2_data_science.section03_numpy.projects.linear_regression.src.visualization import (
    save_plots,
)


@pytest.mark.parametrize("features,batch_size", [(1, None), (3, None), (3, 16)])
def test_fit(tmp_path, features, batch_size):
    X = np.random.default_rng(7).normal(size=(128, features))
    weights = np.arange(1.0, features + 1)
    y = X @ weights + 2
    model = LinearRegression(epochs=250, batch_size=batch_size).fit(
        X[:, 0] if features == 1 else X, y
    )
    np.testing.assert_allclose(model.weights_, weights, atol=1e-6)
    assert model.bias_ == pytest.approx(2, abs=1e-6)
    assert mse_loss(y, model.predict(X)) < 1e-10
    assert model.loss_history_[-1] < model.loss_history_[0]
    save_plots(model.loss_history_, y, model.predict(X), tmp_path)
    assert (tmp_path / "training.png").read_bytes().startswith(b"\x89PNG")


@pytest.mark.parametrize("features", [1, 2, 4])
def test_gradient_finite_difference(features):
    rng = np.random.default_rng(13)
    X = rng.normal(size=(5, features))
    y = rng.normal(size=5)
    weights = rng.normal(size=features)
    bias = 0.7
    dw, db = gradients(X, y, weights, bias)
    epsilon = 1e-6
    for i in range(features):
        delta = np.zeros(features)
        delta[i] = epsilon
        numerical = (
            mse_loss(y, X @ (weights + delta) + bias) - mse_loss(y, X @ (weights - delta) + bias)
        ) / (2 * epsilon)
        assert dw[i] == pytest.approx(numerical, rel=1e-5, abs=1e-7)
    numerical = (
        mse_loss(y, X @ weights + bias + epsilon) - mse_loss(y, X @ weights + bias - epsilon)
    ) / (2 * epsilon)
    assert db == pytest.approx(numerical, rel=1e-5)


@pytest.mark.parametrize("kwargs", [{"epochs": 0}, {"batch_size": 0}, {"learning_rate": -1}])
def test_invalid(kwargs):
    with pytest.raises(ValueError):
        LinearRegression(**kwargs)
