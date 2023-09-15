# Use the Python 3.9 slim image as the base image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the host into the container's /app directory
COPY requirements.txt /app

# Upgrade pip 
RUN pip install --upgrade pip

# Download pytorch CPU
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download the image features from a Google Drive link
RUN gdown https://drive.google.com/uc?id=1-3CH-0PZbNziCH3JYwZcOTyqhThhe8wg

# Move the downloaded index to a directory named /faiss_store
RUN mkdir --parents /app/faiss_store && mv index.faiss /app/faiss_store

# Download model
RUN python -c 'from torchvision.models import efficientnet_b3, EfficientNet_B3_Weights; efficientnet_b3(weights=EfficientNet_B3_Weights.IMAGENET1K_V1)'

# Copy all files from the host into the container's /app directory
COPY . /app

# Expose port 7000 to the host machine
EXPOSE 7000

# Run the uvicorn server to start the application when the container is started
CMD uvicorn app:app --port 7000 --host 0.0.0.0
