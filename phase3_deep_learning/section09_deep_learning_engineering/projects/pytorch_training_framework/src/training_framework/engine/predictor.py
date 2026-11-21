"""Image inference needs only a checkpoint and local input, not a config file."""

from pathlib import Path

from PIL import Image
from torchvision import transforms

from phase3_deep_learning.common.engine import probabilities
from phase3_deep_learning.common.runtime import choose_device

from ..datasets.image_folder import image_transforms
from .evaluator import load_model


def predict_image(checkpoint: str | Path, image: str | Path, device: str = "cpu") -> dict:
    """Reapply the saved channel/resize/normalization policy."""
    target = choose_device(device)
    model, state = load_model(checkpoint, target)
    p = state["preprocess"]
    with Image.open(image) as raw:
        if p["normalize"] == "imagenet":
            tensor = image_transforms(p["image_size"], False)(raw)
        else:
            raw = raw.convert("L" if p["channels"] == 1 else "RGB")
            tensor = transforms.ToTensor()(
                transforms.Resize((p["image_size"], p["image_size"]))(raw)
            )
    probs = probabilities(model, tensor.unsqueeze(0), target)[0]
    index = int(probs.argmax())
    return {"index": index, "label": state["classes"][index], "probabilities": probs.tolist()}
