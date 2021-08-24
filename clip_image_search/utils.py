import smart_open
from PIL import Image


def load_image_from_url(image_url):
    with smart_open.open(image_url, "rb") as image_file:
        return pil_loader(image_file)


def pil_loader(image_file):
    with Image.open(image_file) as image:
        return image.convert("RGB")
