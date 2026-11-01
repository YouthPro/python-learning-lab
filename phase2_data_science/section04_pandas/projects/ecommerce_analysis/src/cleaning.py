"""Explicit deterministic policies, without editing source frames."""

import pandas as pd


def table_quality(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": int(df.duplicated().sum()),
        "missing": {
            c: {
                "count": int(df[c].isna().sum()),
                "ratio": float(df[c].isna().mean()) if len(df) else 0.0,
            }
            for c in df
        },
    }


def clean_tables(tables: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], dict]:
    before = {name: table_quality(df) for name, df in tables.items()}
    users = tables["users"].drop_duplicates("user_id", keep="first").copy()
    products = tables["products"].drop_duplicates("product_id", keep="first").copy()
    orders = tables["orders"].drop_duplicates("order_id", keep="first").copy()
    # IDs must be finite positive integers, rather than silently truncating them.
    for frame, columns in [
        (users, ["user_id"]),
        (products, ["product_id"]),
        (orders, ["order_id", "user_id", "product_id"]),
    ]:
        for column in columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
            frame.drop(
                frame.index[~(frame[column].gt(0) & frame[column].mod(1).eq(0))], inplace=True
            )
            frame[column] = frame[column].astype("int64")
    users["age"] = pd.to_numeric(users["age"], errors="coerce")
    invalid_age = ~users["age"].between(18, 100)
    users.loc[invalid_age, "age"] = float("nan")
    age_median = users["age"].median()
    users["age"] = users["age"].fillna(0 if pd.isna(age_median) else age_median)
    for column in ["city", "gender"]:
        users[column] = users[column].fillna("Unknown")
    users["register_date"] = pd.to_datetime(users["register_date"], errors="coerce")
    products["price"] = pd.to_numeric(products["price"], errors="coerce")
    invalid_price = ~products["price"].between(0.01, 10000)
    products.loc[invalid_price, "price"] = float("nan")
    products["category"] = products["category"].fillna("Unknown")
    category_median = products.groupby("category")["price"].transform("median")
    overall = products["price"].median()
    products["price"] = (
        products["price"].fillna(category_median).fillna(0 if pd.isna(overall) else overall)
    )
    products["product_name"] = products["product_name"].fillna("Unnamed")
    orders["quantity"] = pd.to_numeric(orders["quantity"], errors="coerce")
    invalid_quantity = ~(orders["quantity"].between(1, 100) & orders["quantity"].mod(1).eq(0))
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    valid = (
        ~invalid_quantity
        & orders["order_date"].notna()
        & orders["user_id"].isin(users["user_id"])
        & orders["product_id"].isin(products["product_id"])
    )
    orders = orders.loc[valid].copy()
    orders["quantity"] = orders["quantity"].astype("int64")
    cleaned = {
        "users": users.reset_index(drop=True),
        "products": products.reset_index(drop=True),
        "orders": orders.reset_index(drop=True),
    }
    quality = {
        "before": before,
        "after": {name: table_quality(df) for name, df in cleaned.items()},
        "invalid_age": int(invalid_age.sum()),
        "invalid_price": int(invalid_price.sum()),
        "invalid_quantity": int(invalid_quantity.sum()),
        "removed_orders": len(tables["orders"]) - len(orders),
    }
    return cleaned, quality
