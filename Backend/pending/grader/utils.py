import os
import uuid
import base64
import logging
from PIL import Image
from io import BytesIO
logger = logging.getLogger(__name__)

DATA_DIR = "Data/Grader"
MAX_DIMENSION = 1024
JPEG_QUALITY = 85

def resize_image(image_data: bytes, max_dimension: int = MAX_DIMENSION) -> bytes:
    """
    Resize image so the longest side is at most max_dimension (maintains aspect ratio).
    Does not upscale images smaller than max_dimension.

    Args:
        image_data: Raw image bytes.
        max_dimension: Maximum pixel length for the longest side.

    Returns:
        Resized JPEG bytes.
    """
    img = Image.open(BytesIO(image_data))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

    output = BytesIO()
    img.save(output, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    return output.getvalue()

def process_and_save_image(file_content: bytes, filename: str) -> str:
    """
    Saves image to uuid folder, resizes if > 1MB, and returns Base64 string.

    Args:
        file_content: Raw bytes of the uploaded image.
        filename: Original filename to determine extension.

    Returns:
        Base64-encoded string of the (possibly resized) image.
    """
    folder_id = str(uuid.uuid4())
    save_path = os.path.join(DATA_DIR, folder_id)
    os.makedirs(save_path, exist_ok=True)

    file_extension = os.path.splitext(filename)[1].lower() or ".jpg"
    full_file_path = os.path.join(save_path, f"image{file_extension}")

    file_size = len(file_content)
    if file_size > 1024 * 1024:
        logger.info("Resizing image: %s (%d bytes)", filename, file_size)
        processed = resize_image(file_content)
    else:
        img = Image.open(BytesIO(file_content))
        w, h = img.size
        if w > MAX_DIMENSION or h > MAX_DIMENSION:
            logger.info("Resizing large-dimension image: %s (%dx%d)", filename, w, h)
            processed = resize_image(file_content)
        else:
            processed = file_content

    with open(full_file_path, "wb") as f:
        f.write(processed)

    with open(full_file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    return encoded_string