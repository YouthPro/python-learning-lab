"""Array operations preserve uint8/float32 range semantics."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def validate(image: np.ndarray) -> float:
    if image.dtype not in (np.dtype("uint8"), np.dtype("float32")):
        raise TypeError("expected uint8 [0,255] or float32 [0,1]")
    if image.ndim not in (2, 3) or (image.ndim == 3 and image.shape[-1] != 3) or 0 in image.shape:
        raise ValueError("expected nonempty H,W or H,W,3")
    maximum = 255.0 if image.dtype == np.uint8 else 1.0
    if not np.isfinite(image).all() or np.any(image < 0) or np.any(image > maximum):
        raise ValueError("pixels outside expected range")
    return maximum


def _restore(values: np.ndarray, source: np.ndarray) -> np.ndarray:
    clipped = np.clip(values, 0, 255 if source.dtype == np.uint8 else 1)
    return (
        np.rint(clipped).astype(np.uint8)
        if source.dtype == np.uint8
        else clipped.astype(np.float32)
    )


def grayscale(image: np.ndarray) -> np.ndarray:
    validate(image)
    if image.ndim == 2:
        return image.copy()
    return _restore(
        image.astype(np.float32) @ np.array([0.299, 0.587, 0.114], dtype=np.float32), image
    )


def brightness(image: np.ndarray, factor: float) -> np.ndarray:
    validate(image)
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("factor must be finite and nonnegative")
    return _restore(image.astype(np.float32) * factor, image)


def contrast(image: np.ndarray, factor: float) -> np.ndarray:
    validate(image)
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("factor must be finite and nonnegative")
    pixels = image.astype(np.float32)
    center = pixels.mean(axis=(0, 1), keepdims=True)
    return _restore((pixels - center) * factor + center, image)


def normalize(image: np.ndarray) -> np.ndarray:
    maximum = validate(image)
    return image.astype(np.float32) / maximum


def crop(image: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    validate(image)
    left, top, right, bottom = box
    if not (0 <= left < right <= image.shape[1] and 0 <= top < bottom <= image.shape[0]):
        raise ValueError("invalid crop box")
    return image[top:bottom, left:right].copy()


def rotate(image: np.ndarray, k: int = 1) -> np.ndarray:
    validate(image)
    return np.rot90(image, -k, axes=(0, 1)).copy()


def process_batch(
    paths: list[str | Path], output: str | Path, operation: str, **kwargs
) -> list[Path]:
    functions = {
        "grayscale": grayscale,
        "brightness": brightness,
        "contrast": contrast,
        "normalize": normalize,
        "crop": crop,
        "rotate": rotate,
    }
    if operation not in functions:
        raise ValueError("unknown operation")
    root = Path(output)
    targets = [root / (Path(p).stem + ".png") for p in paths]
    if len(set(targets)) != len(targets):
        raise ValueError("input stems must be unique")
    if any(t.resolve() == Path(p).resolve() for p, t in zip(paths, targets)):
        raise ValueError("output must differ from input")
    root.mkdir(parents=True, exist_ok=True)
    for source, target in zip(paths, targets):
        with Image.open(source) as image:
            arr = np.asarray(image.convert("RGB"))
        result = functions[operation](arr, **kwargs)
        pixels = np.rint(result * 255).astype(np.uint8) if result.dtype == np.float32 else result
        Image.fromarray(pixels).save(target)
    return targets


def main(argv=None):
    p = argparse.ArgumentParser(description="NumPy image processing")
    p.add_argument("paths", nargs="+")
    p.add_argument("--output", required=True)
    p.add_argument(
        "--operation",
        choices=["grayscale", "brightness", "contrast", "normalize", "crop", "rotate"],
        default="grayscale",
    )
    p.add_argument("--factor", type=float, default=1.2)
    p.add_argument("--box", nargs=4, type=int, default=[0, 0, 16, 16])
    p.add_argument("--k", type=int, default=1)
    args = p.parse_args(argv)
    options = (
        {"factor": args.factor}
        if args.operation in {"brightness", "contrast"}
        else {"box": tuple(args.box)}
        if args.operation == "crop"
        else {"k": args.k}
        if args.operation == "rotate"
        else {}
    )
    try:
        result = process_batch(args.paths, args.output, args.operation, **options)
    except (OSError, ValueError, TypeError) as exc:
        p.exit(2, f"{exc}\n")
    print("\n".join(map(str, result)))


if __name__ == "__main__":
    main()
