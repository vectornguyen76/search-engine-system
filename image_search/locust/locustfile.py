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
    host = "http://localhost:7000"
    # wait_time = constant(1)
    # wait_time = constant_throughput(1)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.image_path = "image_test.jpg"
        # self.request = {"image": encode_img_base64(self.image_path)}

    # @task
    # def search_image_faiss(self):
    #     image_file = open(self.image_path, "rb")
    #     self.client.post("/search-image-faiss", files={"file": image_file})

    # @task
    # def search_image_qdrant(self):
    #     image_file = open(self.image_path, "rb")
    #     self.client.post("/search-image-qdrant", files={"file": image_file})

    @task
    def search_image(self):
        with open(self.image_path, "rb") as image_file:
            self.client.post("/search-image-test", files={"file": image_file})

    # @task
    # def search_image_base64(self):
    #     self.client.post("/search-image-base64", json=self.request)
