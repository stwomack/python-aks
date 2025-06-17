#!/bin/bash

echo "Checking pod status in your-namespace..."
kubectl get pods -n your-namespace

echo "Getting detailed pod information..."
kubectl describe pods -n your-namespace

echo "Checking logs for Temporal worker connectivity..."
POD_NAME=$(kubectl get pods -n your-namespace -l app=your-app -o jsonpath='{.items[0].metadata.name}')
if [ ! -z "$POD_NAME" ]; then
    echo "Checking logs for pod: $POD_NAME"
    kubectl logs $POD_NAME -n your-namespace
else
    echo "No pods found with label app=your-app"
fi