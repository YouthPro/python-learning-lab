import matplotlib.pyplot as plt
import numpy as np
import pytest
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

import phase2_data_science.section06_sklearn.exercises.model_evaluation as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("true,pred", [([1, 2], [1, 2]), ([0, 2], [1, 1]), ([3, 3], [2, 2])])
def test_regression_metrics(true, pred):
    result = m.regression_metrics(np.array(true), np.array(pred))
    assert result == pytest.approx(
        {
            "mae": mean_absolute_error(true, pred),
            "mse": mean_squared_error(true, pred),
            "r2": r2_score(true, pred),
        }
    )
    assert all(isinstance(v, float) for v in result.values())


@pytest.mark.parametrize("true,pred", [([0, 1], [0, 1]), ([0, 0], [0, 0]), ([0, 1, 1], [1, 0, 1])])
def test_classification_metrics(true, pred):
    expected = {
        "accuracy": accuracy_score(true, pred),
        "precision": precision_score(true, pred, zero_division=0),
        "recall": recall_score(true, pred, zero_division=0),
        "f1": f1_score(true, pred, zero_division=0),
    }
    assert m.classification_metrics(np.array(true), np.array(pred)) == pytest.approx(expected)


@pytest.mark.parametrize("true,pred", [([0, 1], [0, 1]), ([0, 0], [0, 0]), ([0, 1, 1], [1, 0, 1])])
def test_confusion(true, pred):
    fig, ax = m.plot_confusion_matrix(np.array(true), np.array(pred))
    try:
        np.testing.assert_array_equal(
            ax.images[0].get_array(), confusion_matrix(true, pred, labels=[0, 1])
        )
        assert ax.get_title()
    finally:
        plt.close(fig)
