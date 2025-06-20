# Configuration Management

This project now uses a centralized configuration system to manage all environment variables in one place.

## Configuration File

All environment variables are defined in `config.env`. This file contains:

- Azure configuration (subscription ID, ACR name, resource group)
- Temporal configuration (address, namespace, task queue, API key)
- Kubernetes configuration (namespace, app name, image)
- Resource limits (CPU and memory)

## Usage

### For Shell Scripts

All shell scripts now source the centralized configuration:

```bash
# Source the config in any script
source ./source_config.sh

# Now all variables are available
echo "Using namespace: $KUBERNETES_NAMESPACE"
echo "Using app name: $APP_NAME"
```

### For Python Applications

Python applications can use the `config` module:

```python
from config import TEMPORAL_ADDRESS, TEMPORAL_NAMESPACE

# Or load the entire config
from config import CONFIG
print(CONFIG['AZURE_SUBSCRIPTION_ID'])
```

### Available Scripts

1. **`source_config.sh`** - Sources the config file and validates required variables
2. **`generate-k8s-manifests.sh`** - Generates Kubernetes manifests from the config
3. **`deploy.sh`** - Deploys the application using the centralized config
4. **`validate.sh`** - Validates the deployment using the centralized config

## Setup

1. Copy `config.env.example` to `config.env` (if available)
2. Update the values in `config.env` with your actual configuration
3. Run your scripts as usual - they will automatically use the centralized config

## Environment Variable Priority

1. System environment variables (highest priority)
2. Values from `config.env` file
3. Default values (lowest priority)

This allows you to override config values with environment variables when needed.

## Required Variables

The following variables are validated by `source_config.sh`:

- `AZURE_SUBSCRIPTION_ID`
- `ACR_NAME`
- `RESOURCE_GROUP`
- `TEMPORAL_ADDRESS`
- `TEMPORAL_NAMESPACE`
- `TEMPORAL_TASK_QUEUE`
- `TEMPORAL_API_KEY`
- `KUBERNETES_NAMESPACE`
- `APP_NAME`
- `APP_IMAGE`

## Example config.env

```bash
# Azure Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
ACR_NAME=womackecr
RESOURCE_GROUP=aks-temporal

# Temporal Configuration
TEMPORAL_ADDRESS=localhost:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=test-task-queue
TEMPORAL_API_KEY=demo-api-key-here

# Kubernetes Configuration
KUBERNETES_NAMESPACE=your-namespace
APP_NAME=demo-app
APP_IMAGE=demo-app:latest

# Resource Limits
CPU_LIMIT=0.5
MEMORY_LIMIT=512Mi
CPU_REQUEST=0.2
MEMORY_REQUEST=256Mi
``` 