"""Explicit --apply required for writes."""

import argparse
import json
import logging

from .operations import (
    batch_rename,
    calculate_file_hash,
    find_duplicates,
    list_files,
    merge_csv,
    normalize_file,
)


def main(argv=None):
    parser = argparse.ArgumentParser(description="File toolkit (writes default to dry-run)")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["scan", "hash", "duplicates"]:
        p = sub.add_parser(name)
        p.add_argument("path")
    p = sub.add_parser("rename")
    p.add_argument("path")
    p.add_argument("--mapping", required=True, help="JSON object of direct filenames")
    p.add_argument("--apply", action="store_true")
    p = sub.add_parser("merge")
    p.add_argument("paths", nargs="+")
    p.add_argument("--output", required=True)
    p.add_argument("--apply", action="store_true")
    p = sub.add_parser("normalize")
    p.add_argument("path")
    p.add_argument("--output", required=True)
    p.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        if args.command == "scan":
            result = list_files(args.path)
        elif args.command == "hash":
            result = calculate_file_hash(args.path)
        elif args.command == "duplicates":
            result = find_duplicates(args.path)
        elif args.command == "rename":
            result = batch_rename(args.path, json.loads(args.mapping), not args.apply)
        elif args.command == "merge":
            result = merge_csv(args.paths, args.output, not args.apply)
        else:
            result = normalize_file(args.path, args.output, not args.apply)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        logging.error("%s", exc)
        parser.exit(2, f"{exc}\n")
    print(json.dumps(result, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
