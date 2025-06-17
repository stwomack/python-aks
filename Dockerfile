# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Temporal Python SDK
RUN pip install --no-cache-dir temporalio

# Copy application code
COPY . .

# Configure Python for unbuffered output
ENV PYTHONUNBUFFERED=1

# Execute the worker
CMD ["python", "worker.py"]