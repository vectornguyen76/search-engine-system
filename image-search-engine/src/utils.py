import base64
import logging
from datetime import datetime

import cv2
import numpy as np
import pytz
from config import settings
from torchvision import transforms


async def save_image_file(file):
    # Prepend the current datetime to the filename
    file.filename = datetime.now().strftime("%Y%m%d-%H%M%S-") + file.filename

    # Construct the full image path based on the settings
    image_path = settings.IMAGEDIR + file.filename

    # Read the contents of the uploaded file asynchronously
    contents = await file.read()

    # Write the uploaded contents to the specified image path
    with open(image_path, "wb") as f:
        f.write(contents)

    return image_path


def decode_img(img: str) -> np.ndarray:
    image_array = np.frombuffer(base64.urlsafe_b64decode(img), dtype=np.uint8)
    # Decode the image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Convert BGR image to RGB image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define a transform to convert
    # the image to torch tensor
    transform = transforms.Compose([transforms.ToTensor()])

    # Convert the image to Torch tensor
    tensor = transform(image)
    return tensor


def initial_logger():
    # Create a logger instance
    logger = logging.getLogger("app")

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Set the timezone to Vietnam
    vietnam_timezone = pytz.timezone("Asia/Ho_Chi_Minh")

    # Configure logging with the Vietnam timezone
    logging.Formatter.converter = (
        lambda *args: pytz.utc.localize(datetime.utcnow())
        .astimezone(vietnam_timezone)
        .timetuple()
    )

    # Define the log format
    console_log_format = "%(asctime)s - %(levelname)s - %(message)s"
    file_log_format = (
        "%(asctime)s - %(levelname)s - %(message)s - (%(filename)s:%(lineno)d)"
    )

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter(console_log_format, datefmt=settings.DATE_FMT)
    )
    logger.addHandler(console_handler)

    # Create a file handler
    file_handler = logging.FileHandler(filename=settings.LOG_DIR, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(file_log_format, datefmt=settings.DATE_FMT)
    )
    logger.addHandler(file_handler)

    return logger


LOGGER = initial_logger()
