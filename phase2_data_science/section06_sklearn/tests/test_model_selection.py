import numpy as np
import pytest
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score

import phase2_data_science.section06_sklearn.exercises.model_selection as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("seed", [0, 17, 42])
def test_cv(seed):
    X = np.arange(60.0).reshape(30, 2)
    y = X[:, 0] * 2 + 1
    model = LinearRegression()
    expected = cross_val_score(
        model, X, y, cv=KFold(3, shuffle=True, random_state=seed), scoring="r2"
    )
    np.testing.assert_allclose(m.evaluate_cv(model, X, y, random_state=seed), expected)
    assert not hasattr(model, "coef_")


@pytest.mark.parametrize("alphas", [[0.1, 1.0], [1.0], [0.01, 0.1, 1.0]])
def test_search(alphas):
    X = np.arange(60.0).reshape(30, 2)
    y = X[:, 0] * 2 + 1
    model = Ridge()
    params = {"alpha": alphas}
    result = m.search_best_params(model, params, X, y, random_state=19)
    expected = GridSearchCV(
        model, params, cv=KFold(3, shuffle=True, random_state=19), scoring="r2", error_score="raise"
    ).fit(X, y)
    assert result.best_params_ == expected.best_params_
    np.testing.assert_allclose(result.predict(X), expected.predict(X))
    assert not hasattr(model, "coef_")
