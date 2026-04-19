FROM python:3.11-slim

# Install pandoc for high-quality EPUB conversion
RUN apt-get update && apt-get install -y pandoc && rm -rf /var/lib/apt/lists/*

# Install required Python libraries
RUN pip install instapaper requests

WORKDIR /app
COPY sync.py .
COPY style.css .

CMD ["python", "sync.py"]
