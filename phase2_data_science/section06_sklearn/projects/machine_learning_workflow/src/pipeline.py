"""Select on training CV only; evaluate the chosen model once on holdout."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)

from .data_loader import load_dataset
from .evaluation import evaluate
from .models import build_models
from .preprocessing import build_pipeline
from .visualization import save_eda, save_evaluation


def train_workflow(config: dict, task: str, output: str | Path) -> dict:
    seed = int(config.get("random_state", 42))
    settings = config[task]
    X, y = load_dataset(task, settings.get("input"), seed, int(settings.get("n_samples", 500)))
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=float(config.get("test_size", 0.2)),
        random_state=seed,
        stratify=y if task == "classification" else None,
    )
    cv_class = StratifiedKFold if task == "classification" else KFold
    cv = cv_class(n_splits=int(config.get("cv_folds", 3)), shuffle=True, random_state=seed)
    scoring = "f1" if task == "classification" else "neg_root_mean_squared_error"
    candidates = []
    searches = {}
    for name, model in build_models(task, seed).items():
        pipeline = build_pipeline(model)
        baseline = cross_val_score(
            pipeline, X_train, y_train, cv=cv, scoring=scoring, error_score="raise", n_jobs=1
        )
        search = GridSearchCV(
            pipeline,
            settings.get("grids", {}).get(name, {}),
            cv=cv,
            scoring=scoring,
            refit=True,
            error_score="raise",
            n_jobs=1,
        )
        search.fit(X_train, y_train)
        candidates.append(
            {
                "name": name,
                "baseline_cv_mean": float(baseline.mean()),
                "tuned_cv_mean": float(search.best_score_),
                "best_params": search.best_params_,
            }
        )
        searches[name] = search
    selected = max(candidates, key=lambda row: row["tuned_cv_mean"])
    best = searches[selected["name"]].best_estimator_
    predictions = best.predict(X_test)
    metrics = evaluate(task, y_test, predictions)
    root = Path(output)
    models, reports = root / "models", root / "reports"
    models.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    model_path = models / f"{task}.joblib"
    joblib.dump(best, model_path)
    result = {
        "task": task,
        "random_state": seed,
        "selected_model": selected["name"],
        "cv_scoring": scoring,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "metrics": metrics,
        "candidates": candidates,
        "train_indices": X_train.index.tolist(),
        "test_indices": X_test.index.tolist(),
    }
    (reports / f"{task}_metrics.json").write_text(
        json.dumps(result, indent=2, allow_nan=False), encoding="utf-8"
    )
    pd.DataFrame(candidates).to_csv(reports / f"{task}_model_comparison.csv", index=False)
    for name, search in searches.items():
        pd.DataFrame(search.cv_results_).to_csv(reports / f"{task}_{name}_search.csv", index=False)
    pd.DataFrame(
        {"actual": y_test.to_numpy(), "prediction": predictions}, index=y_test.index
    ).to_csv(reports / f"{task}_predictions.csv", index_label="row_index")
    save_eda(X_train, y_train, reports / task)
    save_evaluation(task, y_test, predictions, reports / f"{task}_evaluation.png")
    # Exercise the persisted pipeline immediately, including preprocessing state.
    loaded = joblib.load(model_path)
    if not (loaded.predict(X_test) == predictions).all():
        raise RuntimeError("persisted model predictions differ")
    return result


def predict_file(
    model_path: str | Path, input_path: str | Path, output: str | Path
) -> pd.DataFrame:
    pipeline = joblib.load(model_path)
    X = pd.read_csv(input_path)
    columns = list(pipeline.feature_names_in_)
    missing = set(columns) - set(X)
    if missing:
        raise ValueError(f"missing features: {sorted(missing)}")
    features = X.loc[:, columns].apply(pd.to_numeric, errors="coerce")
    result = pd.DataFrame({"prediction": pipeline.predict(features)})
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(path, index=False)
    return result
