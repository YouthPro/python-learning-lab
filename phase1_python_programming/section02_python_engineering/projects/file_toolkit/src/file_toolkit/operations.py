"""All mutations preflight first. No directories or symlinks are renamed."""

import csv
import hashlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def list_files(path: str | Path) -> list[Path]:
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(root)
    if not root.is_dir():
        raise NotADirectoryError(root)
    return sorted((p for p in root.rglob("*") if p.is_file() and not p.is_symlink()), key=str)


def calculate_file_hash(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def find_duplicates(directory: str | Path) -> list[list[Path]]:
    buckets = {}
    for path in list_files(directory):
        key = (path.stat().st_size, calculate_file_hash(path))
        buckets.setdefault(key, []).append(path)
    return sorted([group for group in buckets.values() if len(group) > 1], key=lambda g: str(g[0]))


def normalize_json(data: object) -> object:
    if isinstance(data, dict):
        return {key: normalize_json(data[key]) for key in sorted(data)}
    if isinstance(data, list):
        return [normalize_json(value) for value in data]
    return data.strip() if isinstance(data, str) else data


def _child(root: Path, name: str) -> Path:
    if not name or name in {".", ".."} or Path(name).name != name or "/" in name or "\\" in name:
        raise ValueError("only direct child filenames allowed")
    path = root / name
    if path.is_symlink():
        raise ValueError("symlinks are not supported")
    return path


def batch_rename(
    directory: str | Path, mapping: dict[str, str], dry_run: bool = True
) -> list[tuple[Path, Path]]:
    root = Path(directory)
    if not root.is_dir():
        raise NotADirectoryError(root)
    plan = []
    targets = set()
    for old, new in mapping.items():
        source, target = _child(root, old), _child(root, new)
        if not source.is_file():
            raise FileNotFoundError(source)
        if source == target:
            continue
        if target in targets:
            raise ValueError("duplicate destination")
        if target.exists():
            raise FileExistsError(target)
        targets.add(target)
        plan.append((source, target))
    for source, target in plan:
        logger.info("%srename %s -> %s", "dry-run: " if dry_run else "", source, target)
        if not dry_run:
            # Exclusive hard-link creation prevents accidental overwrite at execution time.
            target.hardlink_to(source)
            source.unlink()
    return plan


def merge_csv(paths: list[str | Path], output: str | Path, dry_run: bool = True) -> int:
    """Validate every header; return data row count; never overwrite output."""
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    header = None
    count = 0
    for path in paths:
        with Path(path).open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            current = next(reader, None)
            if current is None:
                raise ValueError("CSV must contain a header")
            if header is None:
                header = current
            elif header != current:
                raise ValueError("CSV headers must match")
            for row in reader:
                if len(row) != len(header):
                    raise ValueError("CSV row width does not match header")
                count += 1
    if header is None:
        raise ValueError("at least one CSV is required")
    if not dry_run:
        output.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive open also avoids overwriting a destination created after preflight.
        with output.open("x", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            for path in paths:
                with Path(path).open(encoding="utf-8", newline="") as source:
                    reader = csv.reader(source)
                    next(reader)
                    writer.writerows(reader)
    logger.info("merge CSV rows=%s dry_run=%s", count, dry_run)
    return count


def normalize_file(source: str | Path, output: str | Path, dry_run: bool = True) -> object:
    data = normalize_json(json.loads(Path(source).read_text(encoding="utf-8")))
    target = Path(output)
    if target.exists():
        raise FileExistsError(target)
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
    logger.info("normalize JSON %s dry_run=%s", target, dry_run)
    return data
