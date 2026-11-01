"""Deterministic offline datasets. Run from any cwd via this script's absolute path."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def ecommerce(
    output: Path, seed: int = 42, n_users: int = 1000, n_products: int = 100, n_orders: int = 10000
) -> dict:
    if min(n_users, n_products, n_orders) <= 0:
        raise ValueError("positive dataset sizes required")
    rng = np.random.default_rng(seed)
    users = [
        dict(
            user_id=i + 1,
            age=int(rng.integers(18, 71)),
            gender=str(rng.choice(["F", "M"])),
            city=str(rng.choice(["Beijing", "Shanghai", "Shenzhen", "Chengdu", "Hangzhou"])),
            register_date=str(
                np.datetime64("2022-01-01") + np.timedelta64(int(rng.integers(0, 730)), "D")
            ),
        )
        for i in range(n_users)
    ]
    products = [
        dict(
            product_id=i + 1,
            product_name=f"Product {i + 1:03d}",
            category=str(rng.choice(["Books", "Electronics", "Home", "Sports"])),
            price=round(float(rng.uniform(10, 2000)), 2),
        )
        for i in range(n_products)
    ]
    orders = [
        dict(
            order_id=i + 1,
            user_id=int(rng.integers(1, n_users + 1)),
            product_id=int(rng.integers(1, n_products + 1)),
            quantity=int(rng.integers(1, 6)),
            order_date=str(
                np.datetime64("2024-01-01") + np.timedelta64(int(rng.integers(0, 731)), "D")
            ),
        )
        for i in range(n_orders)
    ]
    # Separate corruption streams keep the policy easy to inspect and reproduce.
    for table, column in [
        (users, "age"),
        (users, "city"),
        (products, "price"),
        (orders, "quantity"),
    ]:
        for index in rng.choice(len(table), max(1, len(table) // 100), replace=False):
            table[int(index)][column] = ""
    users[0]["age"] = -20
    products[0]["price"] = -99
    products[-1]["price"] = 1000000
    orders[0]["quantity"] = -2
    orders[1 if n_orders > 1 else 0]["quantity"] = 100000
    for table in [users, products, orders]:
        table.extend(dict(table[i]) for i in range(max(1, len(table) // 100)))
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in [("users", users), ("products", products), ("orders", orders)]:
        write_csv(output / f"{name}.csv", list(rows[0]), rows)
    return {"users": len(users), "products": len(products), "orders": len(orders)}


def housing(output: Path, seed: int = 42, size: int = 600) -> None:
    if size <= 0:
        raise ValueError("size must be positive")
    rng = np.random.default_rng(seed)
    area = rng.uniform(35, 240, size)
    bedrooms = rng.integers(1, 6, size)
    bathrooms = rng.integers(1, 4, size)
    age = rng.uniform(0, 60, size)
    distance = rng.uniform(1, 50, size)
    score = rng.uniform(1, 10, size)
    price = (
        200000
        + area * 4500
        + bedrooms * 16000
        + bathrooms * 22000
        - age * 1800
        - distance * 4000
        + score * 25000
        + rng.normal(0, 18000, size)
    )
    columns = [
        "area",
        "bedrooms",
        "bathrooms",
        "house_age",
        "distance_to_city",
        "location_score",
        "price",
    ]
    rows = [
        dict(zip(columns, map(float, values)))
        for values in zip(area, bedrooms, bathrooms, age, distance, score, price)
    ]
    for column in ["area", "house_age", "location_score"]:
        for index in rng.choice(size, max(1, size // 50), replace=False):
            rows[int(index)][column] = ""
    write_csv(output / "housing.csv", columns, rows)


def classification(output: Path, seed: int = 42, size: int = 500) -> None:
    from sklearn.datasets import make_classification

    X, y = make_classification(
        n_samples=size, n_features=10, n_informative=6, n_redundant=2, random_state=seed
    )
    columns = [f"feature_{i}" for i in range(X.shape[1])] + ["target"]
    rows = [dict(zip(columns, [*map(float, row), int(target)])) for row, target in zip(X, y)]
    write_csv(output / "classification.csv", columns, rows)


def training_logs(output: Path, seed: int = 42, epochs: int = 50) -> None:
    if epochs <= 0:
        raise ValueError("epochs must be positive")
    rng = np.random.default_rng(seed)
    rows = []
    for epoch in range(1, epochs + 1):
        train = 0.9 * np.exp(-epoch / 18) + 0.08
        val = 0.85 * np.exp(-epoch / 17) + 0.12 + max(0, epoch - 25) * 0.012
        rows.append(
            dict(
                epoch=epoch,
                train_loss=float(train + rng.normal(0, 0.004)),
                val_loss=float(val + rng.normal(0, 0.004)),
                train_acc=float(min(0.99, 1 - train * 0.6)),
                val_acc=float(np.clip(1 - val * 0.6, 0, 1)),
                learning_rate=0.01 * (0.5 ** (epoch // 15)),
            )
        )
    write_csv(output / "training_log.csv", list(rows[0]), rows)
    # A second experiment for comparison.
    for row in rows:
        row["val_loss"] *= 0.92
        row["val_acc"] = min(0.99, row["val_acc"] + 0.025)
    write_csv(output / "training_log_b.csv", list(rows[0]), rows)


def generate(output: Path, seed: int = 42, include_classification: bool = True) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    counts = ecommerce(output / "ecommerce", seed)
    housing(output, seed)
    training_logs(output, seed)
    rng = np.random.default_rng(seed)
    np.save(output / "vectors.npy", rng.normal(size=(1000, 128)))
    X = rng.normal(size=(300, 3))
    y = X @ np.array([2.0, -3.0, 0.5]) + 1.5 + rng.normal(0, 0.1, len(X))
    np.savez(output / "regression.npz", X=X, y=y)
    pixels = rng.integers(0, 256, (32, 48, 3), dtype=np.uint8)
    Image.fromarray(pixels).save(output / "sample.png")
    (output / "sample.txt").write_text(
        "Python data science. Python makes data useful.\n", encoding="utf-8"
    )
    if include_classification:
        classification(output, seed)
    manifest = {
        "seed": seed,
        "ecommerce_rows": counts,
        "classification": include_classification,
        "note": "Synthetic educational data; corrupted rows are intentional.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate offline reproducible learning data")
    p.add_argument("--output", type=Path, default=ROOT / "datasets/generated")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--only",
        choices=["all", "core"],
        default="all",
        help="core omits only sklearn classification data",
    )
    args = p.parse_args(argv)
    try:
        manifest = generate(args.output, args.seed, args.only == "all")
    except (OSError, ValueError, ImportError) as exc:
        p.exit(2, f"{exc}\n")
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
