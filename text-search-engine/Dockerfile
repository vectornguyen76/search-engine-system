FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Download load csv data
RUN gdown https://drive.google.com/uc?id=1I-Rv676N45aUgY7tcsazQE7fLzzb2LFr

# Move data.csv to a directory named /data
RUN mkdir --parents /app/data && mv data.csv /app/data

COPY . /app

# Chmod to entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]