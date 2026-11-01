import numpy as np
import pytest
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import phase2_data_science.section06_sklearn.exercises.preprocessing as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("n", [5, 10, 25])
def test_split(n):
    X = np.arange(n * 2).reshape(n, 2)
    y = np.arange(n)
    actual = m.split_dataset(X, y, random_state=17)
    expected = train_test_split(X, y, test_size=0.2, random_state=17)
    for a, b in zip(actual, expected):
        np.testing.assert_array_equal(a, b)
    assert set(actual[2]).isdisjoint(actual[3])


@pytest.mark.parametrize(
    "X", [np.array([[1.0], [3.0]]), np.ones((3, 2)), np.arange(12.0).reshape(4, 3)]
)
def test_scale(X):
    actual, scaler = m.scale_features(X)
    expected = StandardScaler().fit(X)
    np.testing.assert_allclose(actual, expected.transform(X))
    np.testing.assert_allclose(scaler.mean_, expected.mean_)
    np.testing.assert_allclose(scaler.transform(X + 100), expected.transform(X + 100))


@pytest.mark.parametrize(
    "X",
    [
        np.array([[1.0], [np.nan], [3.0]]),
        np.full((2, 1), np.nan),
        np.array([[2.0, 4.0], [4.0, 8.0]]),
    ],
)
def test_preprocess(X):
    pipe = m.build_preprocessing_pipeline()
    assert isinstance(pipe, Pipeline)
    assert list(pipe.named_steps) == ["imputer", "scaler"]
    assert not hasattr(pipe.named_steps["scaler"], "mean_")
    actual = pipe.fit_transform(X)
    expected = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
            ("scaler", StandardScaler()),
        ]
    ).fit_transform(X)
    np.testing.assert_allclose(actual, expected)
    assert m.build_preprocessing_pipeline() is not pipe
