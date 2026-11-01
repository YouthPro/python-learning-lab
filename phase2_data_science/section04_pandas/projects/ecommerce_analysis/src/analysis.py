"""Sales at current catalogue price; this synthetic dataset has no price history."""

import pandas as pd


def analyze(tables: dict[str, pd.DataFrame]) -> dict:
    users, products, orders = (tables[name] for name in ["users", "products", "orders"])
    joined = orders.merge(products, on="product_id", validate="many_to_one").merge(
        users, on="user_id", validate="many_to_one"
    )
    joined["amount"] = joined["price"] * joined["quantity"]
    joined["month"] = joined["order_date"].dt.to_period("M").astype(str)
    monthly = joined.groupby("month", as_index=False).agg(
        sales=("amount", "sum"), orders=("order_id", "count")
    )
    categories = joined.groupby("category", as_index=False).agg(
        sales=("amount", "sum"), quantity=("quantity", "sum")
    )
    product_stats = (
        joined.groupby(["product_id", "product_name", "category"], as_index=False)
        .agg(quantity=("quantity", "sum"), sales=("amount", "sum"))
        .sort_values(["quantity", "product_id"], ascending=[False, True])
    )
    spend = joined.groupby("user_id", as_index=False).agg(
        total_spend=("amount", "sum"), order_count=("order_id", "count")
    )
    customer = users.merge(spend, on="user_id", how="left", validate="one_to_one")
    customer[["total_spend", "order_count"]] = customer[["total_spend", "order_count"]].fillna(0)
    customer = customer.sort_values(["total_spend", "user_id"], ascending=[False, True])
    cities = joined.groupby("city", as_index=False).agg(
        sales=("amount", "sum"), orders=("order_id", "count")
    )
    customer["register_month"] = customer["register_date"].dt.to_period("M").astype("string")
    cohort = (
        customer.assign(buyer=customer["order_count"].gt(0))
        .groupby("register_month", as_index=False)
        .agg(users=("user_id", "count"), buyers=("buyer", "sum"), sales=("total_spend", "sum"))
    )
    cohort["purchase_rate"] = cohort["buyers"] / cohort["users"]
    buyers = customer.loc[customer["order_count"].gt(0), "total_spend"]
    summary = {
        "total_sales": float(joined["amount"].sum()),
        "average_spend_per_user": float(customer["total_spend"].mean()) if len(customer) else 0.0,
        "average_spend_per_buyer": float(buyers.mean()) if len(buyers) else 0.0,
        "order_count": len(joined),
    }
    return {
        "orders_enriched": joined,
        "sales_analysis": monthly,
        "category_analysis": categories,
        "product_analysis": product_stats,
        "customer_analysis": customer,
        "city_analysis": cities,
        "registration_cohorts": cohort,
        "summary": summary,
    }
