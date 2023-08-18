# Use the Python 3.9 slim image as the base image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the host into the container's /app directory
COPY requirements.txt /app

# Upgrade pip and install the Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Download the faiss index from a Google Drive link
RUN gdown https://drive.google.com/uc?id=1-3CH-0PZbNziCH3JYwZcOTyqhThhe8wg

# Move the downloaded index to a directory named /faiss_store
RUN mkdir --parents /app/faiss_store && mv index.faiss /app/faiss_store

# Copy the download_model.py script from the host into the container's /app directory
COPY download_model.py /app

# Run the download_model.py script to download the model
RUN python download_model.py

# Copy all files from the host into the container's /app directory
COPY . /app

# Expose port 7000 to the host machine
EXPOSE 7000

# Run the uvicorn server to start the application when the container is started
CMD uvicorn app:app --port 7000 --host 0.0.0.0
