"""Stable JSON and Markdown representations."""

import json
from pathlib import Path


def to_markdown(report: dict) -> str:
    lines = [
        "# Dataset Summary",
        "",
        f"Rows: {report['rows']}",
        f"Columns: {report['columns']}",
        f"Duplicate Rows: {report['duplicate_rows']}",
        "",
        "## Missing Values",
        "",
    ]
    for column, values in report["missing_values"].items():
        lines.append(f"- {column}: {values['count']} ({values['ratio']:.1%})")
    lines.extend(["", "## Column Statistics", ""])
    for column, values in report["column_statistics"].items():
        lines.extend(
            [
                f"### {column}",
                "",
                f"```json\n{json.dumps(values, ensure_ascii=False, indent=2)}\n```",
                "",
            ]
        )
    return "\n".join(lines)


def save_report(report: dict, output: str | Path) -> None:
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    (root / "summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
    )
    (root / "summary.md").write_text(to_markdown(report), encoding="utf-8")
