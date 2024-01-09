from typing import Any

from locust import FastHttpUser, task


class SearchImageUser(FastHttpUser):
    host = "http://search.vectornguyen.com/backend"

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @task
    def healthz(self):
        self.client.get("/healthz")

    @task
    def create_user(self):
        data = {
            "email": "phuoc@gmail.com",
            "username": "Vector Nguyen",
            "image": "",
            "token": "",
        }

        self.client.post("/auth/users/tokens", json=data)
