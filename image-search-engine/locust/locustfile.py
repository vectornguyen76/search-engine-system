from locust import HttpUser, task


class SearchImageUser(HttpUser):
    @task
    def search_image(self):
        """
        Simulate a user uploading an image and performing a search.
        """

        # Create a random image file
        image_file = open("test.jpg", "rb")

        # Construct the request body
        request_body = {"file": image_file}

        # Send the request to the API and get the response
        self.client.post("/search-image", files=request_body)
