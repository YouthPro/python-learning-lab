import json

import joblib
import numpy as np
import pytest

from phase2_data_science.section06_sklearn.projects.machine_learning_workflow.src.data_loader import (
    load_dataset,
)
from phase2_data_science.section06_sklearn.projects.machine_learning_workflow.src.evaluation import (
    evaluate,
)
from phase2_data_science.section06_sklearn.projects.machine_learning_workflow.src.models import (
    build_models,
)
from phase2_data_science.section06_sklearn.projects.machine_learning_workflow.src.pipeline import (
    predict_file,
    train_workflow,
)
from phase2_data_science.section06_sklearn.projects.machine_learning_workflow.src.preprocessing import (
    build_pipeline,
)
from scripts.generate_datasets import housing


@pytest.mark.parametrize("task", ["regression", "classification"])
@pytest.mark.parametrize("seed", [1, 7, 42])
def test_workflow(tmp_path, task, seed):
    housing(tmp_path, seed, size=80)
    config = {
        "random_state": seed,
        "cv_folds": 2,
        "test_size": 0.25,
        "regression": {
            "input": str(tmp_path / "housing.csv"),
            "grids": {
                "random_forest": {"model__n_estimators": [5]},
                "gradient_boosting": {"model__n_estimators": [5]},
            },
        },
        "classification": {
            "input": None,
            "n_samples": 80,
            "grids": {"random_forest": {"model__n_estimators": [5]}},
        },
    }
    result = train_workflow(config, task, tmp_path / "run")
    assert set(result["train_indices"]).isdisjoint(result["test_indices"])
    assert len(result["candidates"]) == 3
    winner = max(result["candidates"], key=lambda r: r["tuned_cv_mean"])
    assert result["selected_model"] == winner["name"]
    X, y = load_dataset(task, config[task]["input"], seed, 80)
    fitted = joblib.load(tmp_path / f"run/models/{task}.joblib")
    training = X.loc[result["train_indices"]]
    np.testing.assert_allclose(
        fitted.named_steps["imputer"].statistics_, training.median().to_numpy()
    )
    imputed = fitted.named_steps["imputer"].transform(training)
    np.testing.assert_allclose(fitted.named_steps["scaler"].mean_, imputed.mean(axis=0))
    assert fitted.named_steps["scaler"].n_samples_seen_ == result["train_rows"]
    inference = tmp_path / "new.csv"
    X.iloc[:3].to_csv(inference, index=False)
    predicted = predict_file(
        tmp_path / f"run/models/{task}.joblib", inference, tmp_path / "pred.csv"
    )
    np.testing.assert_allclose(predicted["prediction"], fitted.predict(X.iloc[:3]))
    assert (
        json.loads((tmp_path / f"run/reports/{task}_metrics.json").read_text())["metrics"]
        == result["metrics"]
    )


@pytest.mark.parametrize("seed", [1, 7, 42])
def test_build_models_and_no_fit(seed):
    for task in ["regression", "classification"]:
        models = build_models(task, seed)
        assert len(models) == 3
        for model in models.values():
            pipeline = build_pipeline(model)
            assert list(pipeline.named_steps) == ["imputer", "scaler", "model"]
            assert not hasattr(pipeline.named_steps["scaler"], "mean_")


@pytest.mark.parametrize("true,pred", [([0, 1], [0, 1]), ([0, 1], [1, 0]), ([0, 0], [0, 0])])
def test_evaluation(true, pred):
    scores = evaluate("classification", true, pred)
    assert 0 <= scores["accuracy"] <= 1
    assert np.asarray(scores["confusion_matrix"]).sum() == len(true)
    regression = evaluate("regression", true, pred)
    assert regression["rmse"] == pytest.approx(np.sqrt(regression["mse"]))
