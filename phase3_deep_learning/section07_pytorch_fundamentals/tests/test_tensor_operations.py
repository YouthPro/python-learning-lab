import numpy as np
import pytest
import torch

from phase3_deep_learning.section07_pytorch_fundamentals.exercises import tensor_operations as m

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize(
    "data,dtype,expected",
    [
        ([1, 2], None, torch.int64),
        ([[1.0, 2.0]], torch.float64, torch.float64),
        ([], torch.float32, torch.float32),
    ],
)
def test_create_tensor(data, dtype, expected):
    out = m.create_tensor(data, dtype)
    assert out.dtype == expected and out.device.type == "cpu" and not out.requires_grad
    torch.testing.assert_close(out, torch.tensor(data, dtype=expected))


@pytest.mark.parametrize("shape", [(6,), (3, 2), (-1, 1)])
def test_transform_tensor(shape):
    x = torch.arange(6.0, requires_grad=True).reshape(2, 3).T
    out = m.transform_tensor(x, shape)
    torch.testing.assert_close(out, x.reshape(shape))
    assert out.grad_fn is not None
    assert out.shape == x.reshape(shape).shape


@pytest.mark.parametrize("dim,shape", [(0, (1, 2, 3)), (1, (2, 1, 3)), (-1, (2, 3, 1))])
def test_add_batch_dim(dim, shape):
    x = torch.ones(2, 3, requires_grad=True)
    out = m.add_batch_dim(x, dim)
    assert out.shape == shape and out.requires_grad
    torch.testing.assert_close(out.squeeze(dim), x)


@pytest.mark.parametrize(
    "data,expected",
    [([[1.0, 3.0]], [[-1.0, 1.0]]), ([[2.0, 2.0]], [[0.0, 0.0]]), ([[4.0]], [[0.0]])],
)
def test_normalize_last_dim(data, expected):
    x = torch.tensor(data, requires_grad=True)
    out = m.normalize_last_dim(x)
    torch.testing.assert_close(out, torch.tensor(expected))
    assert out.shape == x.shape and out.requires_grad
    out.sum().backward()
    assert torch.isfinite(x.grad).all()


@pytest.mark.parametrize(
    "mask,rows", [([True, False, True], [0, 2]), ([False] * 3, []), ([True] * 3, [0, 1, 2])]
)
def test_select_rows(mask, rows):
    x = torch.arange(6.0).reshape(3, 2).requires_grad_()
    out = m.select_rows(x, torch.tensor(mask))
    torch.testing.assert_close(out, x[rows])
    assert out.shape == (len(rows), 2) and out.requires_grad


@pytest.mark.parametrize(
    "y,expected",
    [
        ([[1.0, 0.0]], [[1.0], [0.0]]),
        ([[0.0, 1.0], [1.0, 0.0]], [[0.0, 1.0], [0.0, 0.0]]),
        ([[0.0, 0.0]], [[0.0], [0.0]]),
        ([[2.0, 2.0]], [[0.70710678], [0.0]]),
    ],
)
def test_pairwise_cosine_similarity(y, expected):
    x = torch.tensor([[1.0, 0.0], [0.0, 0.0]], requires_grad=True)
    out = m.pairwise_cosine_similarity(x, torch.tensor(y))
    torch.testing.assert_close(out, torch.tensor(expected))
    assert out.shape == (2, len(y)) and out.requires_grad


@pytest.mark.parametrize("kind", ["dict", "list", "tuple"])
def test_move_to_device(kind):
    tensor = torch.ones(2, requires_grad=True)
    data = (
        {"x": [tensor, {"v": tensor}], "label": "ok"}
        if kind == "dict"
        else [tensor, "ok"]
        if kind == "list"
        else (tensor, "ok")
    )
    out = m.move_to_device(data, "cpu")
    assert type(out) is type(data) and out is not data
    value = out["x"][1]["v"] if kind == "dict" else out[0]
    torch.testing.assert_close(value, tensor)
    assert value.requires_grad and value.device.type == "cpu"


@pytest.mark.parametrize("dtype", [torch.float32, torch.float64, torch.bfloat16])
def test_to_numpy(dtype):
    x = torch.tensor([1.0, 2.0], dtype=dtype, requires_grad=True)
    out = m.to_numpy(x)
    assert isinstance(out, np.ndarray) and out.shape == (2,)
    assert out.dtype == (np.float64 if dtype == torch.float64 else np.float32)
    np.testing.assert_allclose(out, [1.0, 2.0])
    out[0] = 99
    torch.testing.assert_close(x.detach().float(), torch.tensor([1.0, 2.0]))
