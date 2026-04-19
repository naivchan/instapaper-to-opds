FROM python:3.11-slim

# 1. Install system dependencies (Pandoc)
RUN apt-get update && apt-get install -y \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy and install Python dependencies separately
# This layer is cached! It won't re-run unless requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of your application code
COPY sync.py .
COPY style.css .

CMD ["python", "sync.py"]
