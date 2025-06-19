#!/bin/bash

# Source the centralized configuration
source ./source_config.sh

echo "Checking if namespace $KUBERNETES_NAMESPACE exists..."
if ! kubectl get namespace $KUBERNETES_NAMESPACE >/dev/null 2>&1; then
    echo "Error: Namespace $KUBERNETES_NAMESPACE does not exist!"
    echo "Please run ./deploy.sh first to create the namespace and deploy the application."
    exit 1
fi

echo "Checking pod status in $KUBERNETES_NAMESPACE..."
kubectl get pods -n $KUBERNETES_NAMESPACE

echo "Getting detailed pod information..."
kubectl describe pods -n $KUBERNETES_NAMESPACE

echo "Checking logs for Temporal worker connectivity..."
POD_NAME=$(kubectl get pods -n $KUBERNETES_NAMESPACE -l app=$APP_NAME -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ ! -z "$POD_NAME" ] && [ "$POD_NAME" != "null" ]; then
    echo "Checking logs for pod: $POD_NAME"
    kubectl logs $POD_NAME -n $KUBERNETES_NAMESPACE
else
    echo "No pods found with label app=$APP_NAME"
    echo "This could mean:"
    echo "  1. The deployment hasn't been created yet"
    echo "  2. The pods are still being created"
    echo "  3. The pods failed to start"
    echo ""
    echo "Try running: kubectl get events -n $KUBERNETES_NAMESPACE"
fi