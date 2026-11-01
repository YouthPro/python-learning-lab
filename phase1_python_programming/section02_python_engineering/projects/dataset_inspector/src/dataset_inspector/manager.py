"""CSV/JSON quality statistics with explicit missing-value strategies."""

import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean, median, stdev

DEFAULT_MISSING = ("", "NA", "null", "None")


def is_missing(value, missing_values=DEFAULT_MISSING) -> bool:
    return (
        value is None or (isinstance(value, float) and math.isnan(value)) or value in missing_values
    )


def numeric(value) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


class DatasetManager:
    def __init__(
        self, records: list[dict], columns: list[str] | None = None, missing_values=DEFAULT_MISSING
    ):
        self.columns = list(
            columns if columns is not None else dict.fromkeys(k for r in records for k in r)
        )
        self.records = [{key: r.get(key) for key in self.columns} for r in records]
        self.missing_values = tuple(missing_values)

    @classmethod
    def from_file(cls, path: str | Path, missing_values=DEFAULT_MISSING):
        path = Path(path)
        if path.suffix.lower() == ".csv":
            with path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                columns = reader.fieldnames or []
                if len(set(columns)) != len(columns):
                    raise ValueError("duplicate CSV columns")
                rows = list(reader)
                if any(None in r or any(v is None for v in r.values()) for r in rows):
                    raise ValueError("CSV row width does not match header")
            return cls(rows, columns, missing_values)
        if path.suffix.lower() == ".json":
            rows = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
                raise ValueError("JSON must be a list of objects")
            return cls(rows, missing_values=missing_values)
        raise ValueError("only .csv and .json are supported")

    def clean(self, strategy: str = "keep", fill_value="unknown"):
        if strategy not in {"keep", "drop", "fill"}:
            raise ValueError("strategy must be keep, drop or fill")
        records = []
        for row in self.records:
            absent = [k for k, v in row.items() if is_missing(v, self.missing_values)]
            if strategy == "drop" and absent:
                continue
            records.append(
                {
                    k: (fill_value if strategy == "fill" and k in absent else v)
                    for k, v in row.items()
                }
            )
        return type(self)(records, self.columns, self.missing_values)

    def summary(self) -> dict:
        n = len(self.records)
        seen = set()
        duplicates = 0
        for row in self.records:
            key = json.dumps(row, sort_keys=True, ensure_ascii=False)
            duplicates += key in seen
            seen.add(key)
        missing = {}
        statistics = {}
        for column in self.columns:
            present = [
                r[column] for r in self.records if not is_missing(r[column], self.missing_values)
            ]
            count = n - len(present)
            missing[column] = {"count": count, "ratio": count / n if n else 0.0}
            values = [numeric(v) for v in present]
            if present and all(v is not None for v in values):
                statistics[column] = {
                    "dtype": "numeric",
                    "mean": mean(values),
                    "median": median(values),
                    "min": min(values),
                    "max": max(values),
                    "std": stdev(values) if len(values) > 1 else 0.0,
                }
            else:
                counts = Counter(
                    json.dumps(v, ensure_ascii=False, sort_keys=True)
                    if isinstance(v, (dict, list))
                    else str(v)
                    for v in present
                )
                statistics[column] = {
                    "dtype": "categorical",
                    "unique_values": len(counts),
                    "top_categories": sorted(counts.items(), key=lambda p: (-p[1], p[0]))[:5],
                }
        return {
            "rows": n,
            "columns": len(self.columns),
            "duplicate_rows": duplicates,
            "missing_values": missing,
            "column_statistics": statistics,
        }
