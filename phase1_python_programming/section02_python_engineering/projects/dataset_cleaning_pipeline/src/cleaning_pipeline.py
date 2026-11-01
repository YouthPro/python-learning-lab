"""Composable immutable cleaning steps, using only the standard library."""

import argparse
import csv
import json
from collections.abc import Callable
from pathlib import Path

from phase1_python_programming.section02_python_engineering.projects.dataset_inspector.src.dataset_inspector.manager import (
    DatasetManager,
    is_missing,
)


def fill_missing(rows: list[dict], values: dict) -> list[dict]:
    return [{k: values.get(k, v) if is_missing(v) else v for k, v in r.items()} for r in rows]


def deduplicate(rows: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for row in rows:
        key = json.dumps(row, sort_keys=True)
        if key not in seen:
            result.append(dict(row))
            seen.add(key)
    return result


def convert_types(rows: list[dict], converters: dict[str, Callable]) -> list[dict]:
    return [
        {
            k: converters[k](v) if k in converters and not is_missing(v) else v
            for k, v in row.items()
        }
        for row in rows
    ]


def select_columns(rows: list[dict], columns: list[str]) -> list[dict]:
    return [{k: row[k] for k in columns} for row in rows]


class CleaningPipeline:
    def __init__(self, steps: list[Callable]):
        self.steps = list(steps)

    def run(self, rows: list[dict]) -> list[dict]:
        current = [dict(row) for row in rows]
        for step in self.steps:
            current = step(current)
        return current


def clean_file(
    source: str | Path,
    output: str | Path,
    pipeline: CleaningPipeline,
    columns: list[str] | None = None,
) -> dict:
    manager = DatasetManager.from_file(source)
    clean = pipeline.run(manager.records)
    selected = columns if columns is not None else manager.columns
    if clean and list(clean[0]) != selected:
        raise ValueError("output columns must match pipeline columns")
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=selected)
        writer.writeheader()
        writer.writerows(clean)
    return {"before": manager.summary(), "after": DatasetManager(clean, selected).summary()}


def main(argv=None):
    p = argparse.ArgumentParser(description="Composable CSV cleaning pipeline")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--fill", default="{}", help="JSON column-to-fill-value map")
    p.add_argument("--types", default="{}", help="JSON column-to-int/float/str map")
    p.add_argument("--columns", nargs="+")
    p.add_argument("--report", default="datasets/processed/cleaning_comparison.json")
    args = p.parse_args(argv)
    try:
        fill = json.loads(args.fill)
        types = {
            k: {"int": int, "float": float, "str": str}[v]
            for k, v in json.loads(args.types).items()
        }
        steps = [
            lambda rows: fill_missing(rows, fill),
            deduplicate,
            lambda rows: convert_types(rows, types),
        ]
        if args.columns:
            steps.append(lambda rows: select_columns(rows, args.columns))
        report = clean_file(args.input, args.output, CleaningPipeline(steps), args.columns)
        destination = Path(args.report)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        p.exit(2, f"{exc}\n")
    print(
        json.dumps({"before_rows": report["before"]["rows"], "after_rows": report["after"]["rows"]})
    )


if __name__ == "__main__":
    main()
