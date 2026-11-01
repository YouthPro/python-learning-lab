"""Eight saved figures sharing the Section 04 cleaning contract."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.analysis import analyze
from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.cleaning import (
    clean_tables,
)
from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.data_loader import (
    load_tables,
)


def generate_report(tables: dict, results: dict, output: str | Path) -> list[Path]:
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    users, products = tables["users"], tables["products"]
    figures = []
    descriptions = []

    def save(name, title, xlabel, ylabel, draw, description):
        fig, ax = plt.subplots(figsize=(7, 4))
        try:
            draw(fig, ax)
            ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
            fig.tight_layout()
            path = root / f"{name}.png"
            fig.savefig(path, dpi=150, bbox_inches="tight")
            figures.append(path)
            descriptions.append((title, path.name, description))
        finally:
            plt.close(fig)

    city = users["city"].value_counts()
    category = results["category_analysis"]
    monthly = results["sales_analysis"]
    numeric = results["orders_enriched"].select_dtypes(include="number")
    correlation = numeric.corr()
    save(
        "age",
        "User age distribution",
        "Age",
        "Users",
        lambda f, a: a.hist(users["age"].dropna(), bins=20),
        "观察年龄分布，注意中位数填充可能形成峰值。",
    )
    save(
        "cities",
        "Users by city",
        "City",
        "Users",
        lambda f, a: a.bar(city.index.astype(str), city.values),
        "统计注册用户数量，包含 Unknown 城市。",
    )
    save(
        "prices",
        "Product prices",
        "Price",
        "Products",
        lambda f, a: a.hist(products["price"].dropna(), bins=20),
        "清洗后的商品价格分布。",
    )
    save(
        "category_sales",
        "Sales by category",
        "Category",
        "Revenue",
        lambda f, a: a.bar(category["category"], category["sales"]),
        "金额按当前商品价格计算。",
    )

    def monthly_plot(fig, ax):
        ax.plot(monthly["month"], monthly["sales"], marker="o", label="Sales")
        ax.tick_params(axis="x", rotation=60)
        ax.legend()

    save(
        "monthly_sales",
        "Monthly sales",
        "Month",
        "Revenue",
        monthly_plot,
        "检查月度波动，不能据模拟数据推断现实业务趋势。",
    )
    save(
        "customer_spend",
        "Customer spending",
        "Spend",
        "Users",
        lambda f, a: a.hist(results["customer_analysis"]["total_spend"], bins=20),
        "包含消费为零的注册用户。",
    )

    def heatmap(fig, ax):
        if len(correlation.columns) == 0:
            ax.text(0.5, 0.5, "No numeric features", ha="center")
            return
        image = ax.imshow(correlation.to_numpy(), vmin=-1, vmax=1, cmap="coolwarm")
        ax.set_xticks(range(len(correlation)), correlation.columns, rotation=90)
        ax.set_yticks(range(len(correlation)), correlation.columns)
        fig.colorbar(image, ax=ax)

    save(
        "correlation",
        "Feature correlation",
        "Feature",
        "Feature",
        heatmap,
        "相关不等于因果；ID 列只用于练习解读相关矩阵。",
    )
    save(
        "outliers",
        "Price outliers",
        "Products",
        "Price",
        lambda f, a: a.boxplot(products["price"].dropna().to_numpy()),
        "箱线图的离群点表示 IQR 规则下的候选异常，并非自动判错。",
    )
    lines = ["# Ecommerce exploratory data analysis", ""]
    for title, name, description in descriptions:
        lines.extend([f"## {title}", "", f"![{title}]({name})", "", description, ""])
    (root / "eda_report.md").write_text("\n".join(lines), encoding="utf-8")
    return figures


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate eight EDA figures and Markdown report")
    p.add_argument("--input", default="datasets/generated/ecommerce")
    p.add_argument("--output", default="datasets/processed/eda")
    args = p.parse_args(argv)
    try:
        tables, _ = clean_tables(load_tables(args.input))
        figures = generate_report(tables, analyze(tables), args.output)
    except (OSError, ValueError, KeyError) as exc:
        p.exit(2, f"{exc}\n")
    print(f"{len(figures)} figures saved")


if __name__ == "__main__":
    main()
