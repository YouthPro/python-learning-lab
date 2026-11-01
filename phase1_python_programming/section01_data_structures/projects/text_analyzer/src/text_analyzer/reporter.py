"""JSON 为完整报告；CSV 为所有词频。"""

import csv
import json
from pathlib import Path


def save_report(report: dict, output: str | Path) -> tuple[Path, Path]:
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    json_path, csv_path = root / "analysis.json", root / "word_frequency.csv"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["word", "count"])
        writer.writerows(report["word_frequency"].items())
    return json_path, csv_path
