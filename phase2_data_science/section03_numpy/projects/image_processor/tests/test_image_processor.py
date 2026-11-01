import numpy as np
import pytest
from PIL import Image

from phase2_data_science.section03_numpy.projects.image_processor.src import image_processor as m


@pytest.mark.parametrize("dtype,maximum", [(np.uint8, 255), (np.float32, 1), (np.uint8, 128)])
def test_operations(dtype, maximum):
    image = np.array(
        [[[maximum, 0, 0], [0, maximum, 0]], [[0, 0, maximum], [maximum, maximum, maximum]]],
        dtype=dtype,
    )
    before = image.copy()
    limit = 255 if dtype == np.uint8 else 1
    gray = m.grayscale(image)
    expected = np.array([[0.299, 0.587], [0.114, 1.0]]) * maximum
    np.testing.assert_allclose(gray, expected, atol=1 if dtype == np.uint8 else 1e-6)
    assert gray.dtype == dtype
    np.testing.assert_array_equal(m.brightness(image, 1), image)
    assert m.brightness(image, 2).max() <= limit
    np.testing.assert_array_equal(m.contrast(image, 1), image)
    np.testing.assert_allclose(m.contrast(image, 0)[0, 0], image.mean((0, 1)), atol=1)
    np.testing.assert_allclose(m.normalize(image), image.astype(np.float32) / limit)
    np.testing.assert_array_equal(m.crop(image, (0, 0, 1, 2)), image[:, :1])
    np.testing.assert_array_equal(m.rotate(image), np.rot90(image, -1))
    np.testing.assert_array_equal(image, before)


@pytest.mark.parametrize("operation", ["grayscale", "brightness", "normalize"])
def test_batch(tmp_path, operation):
    p = tmp_path / "image.png"
    Image.fromarray(np.full((4, 5, 3), 120, dtype=np.uint8)).save(p)
    output = m.process_batch(
        [p], tmp_path / "out", operation, **({"factor": 2} if operation == "brightness" else {})
    )
    with Image.open(output[0]) as image:
        assert image.size == (5, 4)
        assert image.mode == ("L" if operation == "grayscale" else "RGB")


@pytest.mark.parametrize(
    "invalid",
    [
        np.zeros((0, 2), dtype=np.uint8),
        np.ones((2, 2, 4), dtype=np.uint8),
        np.full((2, 2), 2, dtype=np.float32),
    ],
)
def test_invalid(invalid):
    with pytest.raises(ValueError):
        m.grayscale(invalid)
