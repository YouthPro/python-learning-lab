"""Learner TODOs; project implementations do not import this module."""

from torch import Tensor, nn


def compute_scalar_gradient(x: Tensor) -> Tensor:
    """09. Scalar Gradient.

    Differentiate f(x)=x^3+2*x^2+3*x for a scalar floating tensor; return detached derivative without modifying caller x.grad.
    Input Shape -> Output Shape: [] -> []
    Expected dtype: same floating dtype
    Grad / computation graph: construct fresh leaf, backward then detach result
    Hint: On paper: derivative of each power, then add. Avoid wrapping an existing graph accidentally.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def compute_vector_gradient(x: Tensor) -> Tensor:
    """10. Vector Gradient.

    Differentiate scalar f(x)=sum(x*x+3*x); return detached gradient, do not modify caller x.grad.
    Input Shape -> Output Shape: [*S] -> [*S]
    Expected dtype: same floating dtype
    Grad / computation graph: build scalar reduction before backward
    Hint: Each coordinate contributes independently; explain the chain rule through sum.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def gradient_accumulation_demo(x: Tensor) -> dict[str, Tensor]:
    """11. Gradient Accumulation.

    For fresh scalar leaf and f=x^2, return detached copies: first gradient after one backward, accumulated after second fresh graph backward, after_zero after clearing grad and one more backward. Keys first/accumulated/after_zero.
    Input Shape -> Output Shape: [] -> three scalar tensors
    Expected dtype: same floating dtype
    Grad / computation graph: fresh graph per backward; snapshots must not alias .grad
    Hint: Track addition into .grad, then explain why clearing it changes the third result.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def detach_tensor(x: Tensor) -> Tensor:
    """12. Detach Tensor.

    Return detached tensor sharing storage, not a clone. Explain contrast with no_grad context for future operations.
    Input Shape -> Output Shape: [*S] -> same
    Expected dtype: same as x
    Grad / computation graph: requires_grad=False, grad_fn=None
    Hint: Detach affects this tensor; no_grad affects operations in its context.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError


def freeze_parameters(model: nn.Module) -> nn.Module:
    """13. Freeze Parameters.

    Freeze all parameters in-place and return model; do not change train/eval mode. Input gradients can still exist.
    Input Shape -> Output Shape: module tensors [*S] -> same parameter shapes
    Expected dtype: parameter dtypes unchanged
    Grad / computation graph: parameter grads disabled; graph through differentiable inputs may remain
    Hint: requires_grad and eval control different behavior; explain BatchNorm/dropout.
    """
    # TODO: implement the documented contract.
    raise NotImplementedError
