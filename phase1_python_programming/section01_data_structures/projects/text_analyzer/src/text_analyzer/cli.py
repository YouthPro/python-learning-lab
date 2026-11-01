"""Run with python -m ...text_analyzer.cli."""

import argparse

from .analyzer import analyze_files
from .reporter import save_report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Streaming English TXT analyzer")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--stop-words", nargs="*", default=[])
    parser.add_argument("--output", default="datasets/processed/text_analysis")
    args = parser.parse_args(argv)
    try:
        report = analyze_files(args.paths, set(args.stop_words))
        save_report(report, args.output)
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f"{exc}\n")
    print(f"words={report['total_words']}, unique={report['unique_words']}")


if __name__ == "__main__":
    main()
