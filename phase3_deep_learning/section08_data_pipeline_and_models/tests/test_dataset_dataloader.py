import pytest
import torch
from PIL import Image

from phase3_deep_learning.section08_data_pipeline_and_models.exercises import (
    dataset_dataloader as m,
)

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("n", [1, 3, 7])
def test_CustomDataset(n):
    x = torch.arange(n * 2.0).reshape(n, 2)
    y = torch.arange(n, dtype=torch.long)
    data = m.CustomDataset(x, y, lambda z: z + 1)
    assert len(data) == n
    a, b = data[n - 1]
    torch.testing.assert_close(a, x[n - 1] + 1)
    assert b == y[n - 1]


@pytest.mark.parametrize("n,ratio", [(0, 0.2), (10, 0.3), (7, 0.0)])
def test_split_indices(n, ratio):
    a, b = m.split_indices(n, ratio, 42)
    assert len(b) == int(n * ratio)
    assert not set(a) & set(b) and sorted(a + b) == list(range(n))
    assert (a, b) == m.split_indices(n, ratio, 42)


@pytest.mark.parametrize(
    "labels,k,expected", [([0, 0, 1], 2, [0.75, 1.5]), ([0, 0], 3, [1 / 3, 0, 0]), ([], 2, [0, 0])]
)
def test_compute_class_weights(labels, k, expected):
    out = m.compute_class_weights(torch.tensor(labels, dtype=torch.long), k)
    assert out.dtype == torch.float32 and out.shape == (k,)
    torch.testing.assert_close(out, torch.tensor(expected, dtype=torch.float32))


@pytest.mark.parametrize("lengths", [[1, 3], [0, 2], [0, 0]])
def test_pad_collate(lengths):
    batch = [(torch.arange(n, dtype=torch.float32) + 1, i) for i, n in enumerate(lengths)]
    out = m.pad_collate(batch)
    assert out["inputs"].shape == (2, max(lengths))
    torch.testing.assert_close(out["lengths"], torch.tensor(lengths))
    torch.testing.assert_close(out["targets"], torch.arange(2))
    for i, n in enumerate(lengths):
        torch.testing.assert_close(out["inputs"][i, :n], batch[i][0])
        assert not out["inputs"][i, n:].any()


@pytest.mark.parametrize("extension", ["png", "JPG", "bmp"])
def test_build_image_manifest(tmp_path, extension):
    for name in ["dog", "cat"]:
        folder = tmp_path / name
        folder.mkdir()
        Image.new("RGB", (4, 4)).save(folder / ("x." + extension))
    rows = m.build_image_manifest(tmp_path)
    assert [(a["class_name"], a["label"]) for a in rows] == [("cat", 0), ("dog", 1)]
    assert rows[0]["path"] == "cat/x." + extension


@pytest.mark.parametrize("batch_size", [1, 3, 8])
def test_build_dataloader(batch_size):
    dataset = torch.utils.data.TensorDataset(torch.ones(7, 2), torch.arange(7))
    loader = m.build_dataloader(dataset, batch_size, False, 0)
    batches = list(loader)
    assert sum(len(y) for _, y in batches) == 7 and not loader.pin_memory
    torch.testing.assert_close(torch.cat([y for _, y in batches]), torch.arange(7))
