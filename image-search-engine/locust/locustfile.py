import base64
from typing import Any

import cv2
from locust import FastHttpUser, task


def encode_img_base64(image_path):
    # Load an RGB image using OpenCV
    image = cv2.imread(image_path)

    # Encode the image to a JPEG format (you can choose other formats as well)
    _, encoded_image = cv2.imencode(".jpg", image)

    # Convert the encoded image to a Base64 string
    encoded_image_base64 = base64.b64encode(encoded_image).decode("utf-8")

    return encoded_image_base64


class SearchImageUser(FastHttpUser):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        image_path = "test_image.jpg"
        img_enc = encode_img_base64(image_path)
        self.request = {"image": img_enc}

    @task
    def search_image_base64(self):
        self.client.post("/search-image-base64", json=self.request)

    @task
    def search_image(self):
        image_file = open("test_image.jpg", "rb")
        request_body = {"file": image_file}
        self.client.post("/search-image", files=request_body)
