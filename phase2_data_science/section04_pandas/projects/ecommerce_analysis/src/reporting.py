"""CSV and Markdown artifacts, no optional tabulate dependency."""

import json
from pathlib import Path

import pandas as pd


def save_reports(tables: dict, results: dict, quality: dict, output: str | Path) -> None:
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(root / f"{name}_clean.csv", index=False)
    for name, result in results.items():
        if isinstance(result, pd.DataFrame):
            result.to_csv(root / f"{name}.csv", index=False)
    (root / "summary.json").write_text(
        json.dumps(results["summary"], indent=2, allow_nan=False), encoding="utf-8"
    )
    lines = [
        "# E-commerce data quality and analysis",
        "",
        "策略：主键保留首条；年龄中位数填充；价格按类别中位数填充（其次全局中位数，全部缺失时为 0）；数量限 1..100 整数；无效日期或外键的订单丢弃。",
        "金额按当前商品价格计算。平均用户消费含未购买用户，另提供买家均值。",
        "",
        "## Quality comparison",
        "",
        "```json",
        json.dumps(quality, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Sales summary",
        "",
        "```json",
        json.dumps(results["summary"], indent=2),
        "```",
        "",
        "## Top 10 products by quantity",
        "",
        "```csv",
        results["product_analysis"].head(10).to_csv(index=False),
        "```",
        "",
        "## Top 10 customers by spend",
        "",
        "```csv",
        results["customer_analysis"].head(10).to_csv(index=False),
        "```",
        "",
        "城市销售见 city_analysis.csv，注册月份与购买率见 registration_cohorts.csv。注册时间分析是描述统计，不推断因果。",
    ]
    (root / "data_quality_report.md").write_text("\n".join(lines), encoding="utf-8")
