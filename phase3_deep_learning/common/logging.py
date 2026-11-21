"""Matching CSV and JSONL epoch logs, resumable without duplicate epochs."""

import csv
import json
from pathlib import Path
from typing import Any


def write_history(rows: list[dict[str, Any]], directory: str | Path) -> None:
    """Rewrite small experiment history from authoritative checkpoint history."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with (directory / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (directory / "metrics.jsonl").write_text(
        "".join(json.dumps(row, allow_nan=False) + "\n" for row in rows), encoding="utf-8"
    )
