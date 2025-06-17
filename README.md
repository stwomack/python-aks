# Python Temporal Worker on Azure Kubernetes Service (AKS)

A Python application that runs Temporal workflows and activities, designed for deployment on Azure Kubernetes Service.

## Overview

This project implements a Temporal worker that processes workflows and activities using the Temporal Python SDK. The application is containerized with Docker and configured for deployment on Kubernetes with proper configuration management and resource limits.

## Project Structure

```
├── activities.py      # Temporal activity definitions
├── worker.py         # Main worker application
├── workflows.py      # Temporal workflow definitions
├── Dockerfile        # Container build configuration
├── deployment.yaml   # Kubernetes deployment manifest
├── config-map.yaml   # ConfigMap for environment variables
├── deploy.sh         # Deployment script
└── validate.sh       # Validation script
```

## Components

### Activities (`activities.py`)
- `your_first_activity`: Basic greeting activity
- `your_second_activity`: Data processing activity  
- `your_third_activity`: Final result processing activity

### Workflows (`workflows.py`)
- `YourWorkflow`: Main workflow that orchestrates activity execution

### Worker (`worker.py`)
- Connects to Temporal server
- Registers workflows and activities
- Processes tasks from the configured task queue

## Configuration

The application uses environment variables for configuration:

- `TEMPORAL_ADDRESS`: Temporal server address (default: localhost:7233)
- `TEMPORAL_NAMESPACE`: Temporal namespace (default: default)
- `TEMPORAL_TASK_QUEUE`: Task queue name (default: test-task-queue)
- `TEMPORAL_API_KEY`: API key for Temporal Cloud authentication

## Local Development

### Prerequisites
- Python 3.11+
- Temporal server running locally or Temporal Cloud access

### Setup
```bash
# Install dependencies
pip install temporalio

# Set environment variables
export TEMPORAL_ADDRESS="localhost:7233"
export TEMPORAL_NAMESPACE="default"
export TEMPORAL_TASK_QUEUE="test-task-queue"
export TEMPORAL_API_KEY="your-api-key"

# Run the worker
python worker.py
```

## Kubernetes Deployment

### Prerequisites
- Azure Kubernetes Service cluster
- kubectl configured for your cluster
- Docker registry access

### Deploy
```bash
# Make scripts executable
chmod +x deploy.sh validate.sh

# Deploy to Kubernetes
./deploy.sh

# Validate deployment
./validate.sh
```

### Configuration
Update the following files for your environment:
- `config-map.yaml`: Temporal connection settings
- `deployment.yaml`: Image name, namespace, and resource requirements

## Docker

### Build
```bash
docker build -t your-temporal-worker .
```

### Run
```bash
docker run -e TEMPORAL_ADDRESS=your-address \
           -e TEMPORAL_NAMESPACE=your-namespace \
           -e TEMPORAL_TASK_QUEUE=your-queue \
           -e TEMPORAL_API_KEY=your-key \
           your-temporal-worker
```

## Resource Requirements

The Kubernetes deployment is configured with:
- **Requests**: 0.2 CPU, 256Mi memory
- **Limits**: 0.5 CPU, 512Mi memory

Adjust these values in `deployment.yaml` based on your workload requirements.