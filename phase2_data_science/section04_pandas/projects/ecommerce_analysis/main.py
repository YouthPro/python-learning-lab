import argparse

from .src.analysis import analyze
from .src.cleaning import clean_tables
from .src.data_loader import load_tables
from .src.reporting import save_reports


def main(argv=None):
    p = argparse.ArgumentParser(description="Offline ecommerce analysis")
    p.add_argument("--input", default="datasets/generated/ecommerce")
    p.add_argument(
        "--output",
        default="phase2_data_science/section04_pandas/projects/ecommerce_analysis/reports",
    )
    args = p.parse_args(argv)
    try:
        tables, quality = clean_tables(load_tables(args.input))
        results = analyze(tables)
        save_reports(tables, results, quality, args.output)
    except (OSError, ValueError, KeyError) as exc:
        p.exit(2, f"{exc}\n")
    print(results["summary"])


if __name__ == "__main__":
    main()
