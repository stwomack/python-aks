# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Temporal Python SDK
RUN pip install --no-cache-dir temporalio azure-identity azure-keyvault-secrets cryptography requests

# Copy application code
COPY . /app/

#COPY *.py /app/
#COPY start.sh /app/start.sh
#COPY source_config.sh /app/source_config.sh
#COPY config.env /app/config.env

# Configure Python for unbuffered output
ENV PYTHONUNBUFFERED=1

# Ensure the script is executable
RUN chmod +x /app/start.sh

# Use the script to start both processes
CMD ["bash", "/app/start.sh"]