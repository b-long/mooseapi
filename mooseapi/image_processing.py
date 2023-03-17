import io

from PIL import Image


def decode_image(file: bytes) -> Image:
    return Image.open(io.BytesIO(file)).convert("RGB")
