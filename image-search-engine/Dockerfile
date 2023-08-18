FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY download_model.py /app

# Download model
RUN python download_model.py

COPY . /app

# Run entrypoint.sh
CMD uvicorn app:app --port 5000