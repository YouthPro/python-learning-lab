"""Reference-project seed policy."""

from phase3_deep_learning.common.runtime import seed_all, seed_worker


def seed_everything(seed: int) -> None:
    """Seed all streams and deterministic kernels within the same environment."""
    seed_all(seed)


__all__ = ["seed_everything", "seed_worker"]
