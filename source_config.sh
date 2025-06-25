#!/bin/bash

# Source the configuration file
# This script loads all environment variables from config.env

CONFIG_FILE="config.env"

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file $CONFIG_FILE not found!"
    echo "Please create $CONFIG_FILE with your environment variables."
    exit 1
fi

# Source the config file
echo "Loading configuration from $CONFIG_FILE..."
source "$CONFIG_FILE"

# Validate required variables
required_vars=(
    "AZURE_SUBSCRIPTION_ID"
    "ACR_NAME"
    "RESOURCE_GROUP"
    "TEMPORAL_ADDRESS"
    "TEMPORAL_NAMESPACE"
    "TEMPORAL_TASK_QUEUE"
    "TEMPORAL_API_KEY"
    "KUBERNETES_NAMESPACE"
    "APP_NAME"
    "APP_IMAGE"
    "KEYVAULT_URL"
    "KEYVAULT_SECRET_NAME"
)

echo "Validating required environment variables..."
for var in "${required_vars[@]}"; do
    eval "value=\$$var"
    if [ -z "$value" ]; then
        echo "Warning: $var is not set or empty"
    else
        echo "✓ $var is set"
    fi
done

echo "Configuration loaded successfully!" 