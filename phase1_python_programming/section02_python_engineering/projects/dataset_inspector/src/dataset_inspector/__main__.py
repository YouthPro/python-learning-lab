import argparse

from .manager import DEFAULT_MISSING, DatasetManager
from .reporter import save_report, to_markdown


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect a CSV or JSON dataset")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="datasets/processed/inspection")
    parser.add_argument("--strategy", choices=["keep", "drop", "fill"], default="keep")
    parser.add_argument("--fill-value", default="unknown")
    parser.add_argument("--missing-values", nargs="*", default=list(DEFAULT_MISSING))
    args = parser.parse_args(argv)
    try:
        manager = DatasetManager.from_file(args.input, args.missing_values).clean(
            args.strategy, args.fill_value
        )
        report = manager.summary()
        save_report(report, args.output)
    except (OSError, ValueError, UnicodeError) as exc:
        parser.exit(2, f"{exc}\n")
    print(to_markdown(report))


if __name__ == "__main__":
    main()
