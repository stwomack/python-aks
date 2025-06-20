# Python Temporal Worker on Azure Kubernetes Service (AKS)

A Python application that runs Temporal workflows and activities, designed for deployment on Azure Kubernetes Service.

## Overview

This project implements a Temporal worker that processes workflows and activities using the Temporal Python SDK. The application is containerized with Docker and configured for deployment on Kubernetes with proper configuration management and resource limits.

## Project Structure

```
├── activities.py      # Temporal activity definitions
├── worker.py         # Main worker application
├── workflows.py      # Temporal workflow definitions
├── config.py         # Configuration management module
├── config.env        # Centralized configuration file
├── source_config.sh  # Script to source configuration
├── Dockerfile        # Container build configuration
├── deployment.yaml   # Kubernetes deployment manifest
├── config-map.yaml   # ConfigMap for environment variables
├── deploy.sh         # Deployment script
├── validate.sh       # Validation script
└── generate-k8s-manifests.sh # K8s manifest generator
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

This project uses a centralized configuration system. All environment variables are managed in `config.env`:

### Key Configuration Variables
- `TEMPORAL_ADDRESS`: Temporal server address (default: localhost:7233)
- `TEMPORAL_NAMESPACE`: Temporal namespace (default: default)
- `TEMPORAL_TASK_QUEUE`: Task queue name (default: test-task-queue)
- `TEMPORAL_API_KEY`: API key for Temporal Cloud authentication
- `AZURE_SUBSCRIPTION_ID`: Azure subscription ID
- `ACR_NAME`: Azure Container Registry name
- `RESOURCE_GROUP`: Azure resource group name
- `KUBERNETES_NAMESPACE`: Kubernetes namespace for deployment

For complete configuration details, see [CONFIGURATION.md](CONFIGURATION.md).

## Local Development

### Prerequisites
- Python 3.11+
- Temporal server running locally or Temporal Cloud access

### Setup
```bash
# Install dependencies
pip install config temporalio

# Alternative with venv
python3 -m venv .
source bin/activate
python3 -m pip install config temporalio

# Copy and configure the environment file
cp config.env.example config.env
# Edit config.env with your actual values

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
chmod +x deploy.sh validate.sh generate-k8s-manifests.sh source_config.sh

# Deploy to Kubernetes
./deploy.sh

# Validate deployment
./validate.sh
```

### Configuration
The deployment automatically generates Kubernetes manifests from your `config.env` file. Update the configuration in `config.env` and regenerate manifests:

```bash
./generate-k8s-manifests.sh
```

## Docker

### Build
```bash
docker build -t demo-temporal-worker .
```

### Run
```bash
# The container will automatically use the configuration from config.env
docker run demo-temporal-worker
```

## Resource Requirements

The Kubernetes deployment is configured with:
- **Requests**: 0.2 CPU, 256Mi memory
- **Limits**: 0.5 CPU, 512Mi memory

These values can be adjusted in `config.env` under the Resource Limits section.
