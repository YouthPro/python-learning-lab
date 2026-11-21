"""Learner TODOs; project implementations do not import this module."""

import torch
from torch import Tensor, nn
from torch.utils.data import DataLoader


def build_mlp(input_dim: int, hidden_dims: list[int], num_classes: int) -> nn.Module:
    """14. Build MLP.

    Return Linear/ReLU MLP, final Linear logits, no final Softmax; [] permits linear classifier. Positive dimensions.
    Input Shape -> Output Shape: [B,input_dim] -> [B,num_classes]
    Expected dtype: float32 by default
    Grad / computation graph: trainable parameters and graph
    Hint: List layer dimensions first; CrossEntropyLoss expects logits.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def count_parameters(model: nn.Module) -> int:
    """15. Count Parameters.

    Count ALL parameter elements, including frozen parameters.
    Input Shape -> Output Shape: module -> scalar int
    Expected dtype: Python int
    Grad / computation graph: do not alter gradients
    Hint: Buffers are not parameters; specify whether frozen parameters count.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: str | torch.device,
) -> dict[str, float | int]:
    """16. One Training Epoch.

    Train one epoch with mean-reduced classification loss; zero/backward/step per batch. Return sample-weighted loss, accuracy, samples. Empty loader raises ValueError.
    Input Shape -> Output Shape: batches [B,*S], targets [B] -> statistics
    Expected dtype: float inputs, long targets; Python stats
    Grad / computation graph: training gradients enabled; no graph in returned stats
    Hint: Set train mode, transfer both tensors; last batch may be smaller.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def evaluate(
    model: nn.Module, loader: DataLoader, criterion: nn.Module, device: str | torch.device
) -> dict[str, float | int]:
    """17. Model Evaluation.

    Evaluate mean-loss classification without any gradients; sample-weighted loss/accuracy/samples, restore previous mode; empty loader raises ValueError.
    Input Shape -> Output Shape: batches [B,*S] -> statistics
    Expected dtype: float inputs, long targets
    Grad / computation graph: no_grad/inference_mode; no parameter or grad mutation
    Hint: eval does not disable autograd by itself; multiply mean loss by batch size.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def predict_proba(model: nn.Module, loader: DataLoader, device: str | torch.device) -> Tensor:
    """18. Probability Prediction.

    Return concatenated CPU softmax probabilities in loader order, restore mode. Loader yields (inputs, targets); empty raises ValueError.
    Input Shape -> Output Shape: batches -> [N,num_classes]
    Expected dtype: floating output, rows sum to 1
    Grad / computation graph: no graph, requires_grad=False
    Hint: Apply softmax over classes, not batch; detach before moving outputs.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError
