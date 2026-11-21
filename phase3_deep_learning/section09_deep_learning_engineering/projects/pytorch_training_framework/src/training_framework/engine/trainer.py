"""Epoch orchestration with complete same-environment resume semantics."""

import shutil
from copy import deepcopy
from pathlib import Path
from time import perf_counter

import torch

from phase3_deep_learning.common.engine import train_epoch
from phase3_deep_learning.common.runtime import choose_device
from phase3_deep_learning.common.visualization import plot_history

from ..config import validate_config
from ..datasets import build_data
from ..models import build_model
from ..seed import seed_everything
from ..utils.checkpoint import capture_rng, load_checkpoint, restore_rng, save_state
from ..utils.early_stopping import EarlyStopping
from ..utils.logger import write_history
from .evaluator import evaluate
from .optim import build_optimizer, build_scheduler


class Trainer:
    """Train native MLP/CNN models; best is selected only by validation loss."""

    def __init__(self, config: dict) -> None:
        self.config = validate_config(config)
        self.directory = Path(self.config["run_dir"])
        self.checkpoints = self.directory / "checkpoints"
        self.logs = self.directory / "logs"
        self.history = []

    def _validate_resume(self, state: dict, fingerprint: str) -> None:
        """Permit a longer epoch horizon/device/output path, but no silent objective change."""
        current, old = deepcopy(self.config), deepcopy(state["config"])
        for c in [current, old]:
            for key in ["device", "run_dir", "threads"]:
                c.pop(key)
            c["training"].pop("epochs")
        if current != old or fingerprint != state["fingerprint"]:
            raise ValueError("resume configuration or dataset content/split differs")

    def fit(self, resume: str | Path | None = None) -> list[dict]:
        """Resume at epoch+1, restoring RNG, sampler, optimizer, scheduler and stopper."""
        c = self.config
        if resume is None and any(
            (self.checkpoints / n).exists() for n in ["latest.pt", "best.pt"]
        ):
            raise FileExistsError("run exists; use --resume or a fresh --run-dir")
        torch.set_num_threads(c["threads"])
        seed_everything(c["seed"])
        device = choose_device(c["device"])
        data = build_data(c, persist_split=resume is None)
        model = build_model(c["model"]).to(device)
        optimizer = build_optimizer(model, c["optimizer"])
        scheduler = build_scheduler(optimizer, c["scheduler"])
        enabled = c["training"]["amp"] and device.type == "cuda"
        scaler = torch.amp.GradScaler("cuda", enabled=enabled)
        stop = EarlyStopping(**c["early_stopping"])
        start, best, best_epoch = 1, float("inf"), 0
        if resume is not None:
            state = load_checkpoint(resume)
            self._validate_resume(state, data.fingerprint)
            model.load_state_dict(state["model"])
            optimizer.load_state_dict(state["optimizer"])
            if scheduler is not None:
                scheduler.load_state_dict(state["scheduler"])
            if enabled and state["scaler"]:
                scaler.load_state_dict(state["scaler"])
            stop.load_state_dict(state["early_stopping"])
            self.history = state["history"]
            start = state["epoch"] + 1
            best, best_epoch = state["best_metric"], state["best_epoch"]
            data.train.generator.set_state(state["train_generator"])
            data.validation.generator.set_state(state["val_generator"])
            source_best = Path(resume).parent / "best.pt"
            if not (self.checkpoints / "best.pt").exists():
                if not source_best.is_file():
                    raise ValueError("keep best.pt alongside the resume checkpoint")
                self.checkpoints.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_best, self.checkpoints / "best.pt")
            restore_rng(state["rng"])
            data.save_split(self.directory, c["seed"])
            write_history(self.history, self.logs)
        for epoch in range(start, c["training"]["epochs"] + 1):
            if stop.bad_epochs >= stop.patience:
                break
            started = perf_counter()
            learning_rate = optimizer.param_groups[0]["lr"]
            trained = train_epoch(
                model,
                data.train,
                optimizer,
                device,
                accumulation_steps=c["training"]["gradient_accumulation"],
                max_norm=c["training"]["max_grad_norm"],
                amp=enabled,
                scaler=scaler,
            )
            validated = evaluate(model, data.validation, device)
            if scheduler is not None:
                if isinstance(scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    scheduler.step(validated["loss"])
                else:
                    scheduler.step()
            improved = validated["loss"] < best
            if improved:
                best, best_epoch = validated["loss"], epoch
            should_stop = stop.update(validated["loss"])
            self.history.append(
                {
                    "epoch": epoch,
                    "train_loss": trained["loss"],
                    "val_loss": validated["loss"],
                    "train_accuracy": trained["accuracy"],
                    "val_accuracy": validated["accuracy"],
                    "train_samples": trained["samples"],
                    "val_samples": validated["samples"],
                    "learning_rate": learning_rate,
                    "epoch_duration": perf_counter() - started,
                    "amp_enabled": enabled,
                }
            )
            state = {
                "schema_version": 1,
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "scheduler": scheduler.state_dict() if scheduler else None,
                "scaler": scaler.state_dict(),
                "epoch": epoch,
                "best_metric": best,
                "best_epoch": best_epoch,
                "history": self.history,
                "early_stopping": stop.state_dict(),
                "config": c,
                "model_spec": c["model"],
                "preprocess": data.preprocess,
                "classes": data.classes,
                "fingerprint": data.fingerprint,
                "rng": capture_rng(),
                "train_generator": data.train.generator.get_state(),
                "val_generator": data.validation.generator.get_state(),
            }
            if improved:
                save_state(self.checkpoints / "best.pt", state)
            save_state(self.checkpoints / "latest.pt", state)
            write_history(self.history, self.logs)
            if should_stop:
                break
        if self.history:
            plot_history(self.history, self.directory / "outputs/learning_curves.png")
        return self.history
