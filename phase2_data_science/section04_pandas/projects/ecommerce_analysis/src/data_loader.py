"""Load the three explicit ecommerce schemas."""

from pathlib import Path

import pandas as pd

SCHEMAS = {
    "users": ["user_id", "age", "gender", "city", "register_date"],
    "products": ["product_id", "product_name", "category", "price"],
    "orders": ["order_id", "user_id", "product_id", "quantity", "order_date"],
}


def load_tables(directory: str | Path) -> dict[str, pd.DataFrame]:
    tables = {}
    for name, columns in SCHEMAS.items():
        frame = pd.read_csv(Path(directory) / f"{name}.csv")
        missing = set(columns) - set(frame.columns)
        if missing:
            raise ValueError(f"{name}: missing columns {sorted(missing)}")
        tables[name] = frame.loc[:, columns].copy()
    return tables
