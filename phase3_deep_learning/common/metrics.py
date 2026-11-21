"""Sample-weighted classification metrics and early stopping."""

import math
from dataclasses import dataclass


@dataclass
class RunningMetrics:
    """Aggregate mean batch loss using sample counts, including short batches."""

    loss_sum: float = 0.0
    correct: int = 0
    samples: int = 0

    def update(self, loss: float, correct: int, samples: int) -> None:
        """Add a batch with mean-reduced loss."""
        self.loss_sum += loss * samples
        self.correct += correct
        self.samples += samples

    def result(self) -> dict[str, float | int]:
        """Return loss, accuracy and denominator; reject empty evaluation."""
        if self.samples == 0:
            raise ValueError("loader must contain at least one sample")
        return {
            "loss": self.loss_sum / self.samples,
            "accuracy": self.correct / self.samples,
            "samples": self.samples,
        }


class Stopper:
    """Minimize validation loss; patience counts consecutive non-improvements."""

    def __init__(self, patience: int = 5, min_delta: float = 0.0) -> None:
        if patience < 1 or min_delta < 0:
            raise ValueError("patience >= 1 and min_delta >= 0 required")
        self.patience = patience
        self.min_delta = min_delta
        self.best = math.inf
        self.bad_epochs = 0

    def update(self, loss: float) -> bool:
        """Return whether training should stop."""
        if not math.isfinite(loss):
            raise ValueError("validation loss must be finite")
        if loss < self.best - self.min_delta:
            self.best, self.bad_epochs = loss, 0
        else:
            self.bad_epochs += 1
        return self.bad_epochs >= self.patience

    def state_dict(self) -> dict[str, float | int]:
        """Return resumable early-stopping history."""
        return {"best": self.best, "bad_epochs": self.bad_epochs}

    def load_state_dict(self, state: dict) -> None:
        """Restore counters; hyperparameters come from validated config."""
        self.best = float(state["best"])
        self.bad_epochs = int(state["bad_epochs"])
