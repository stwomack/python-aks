#!/bin/bash

# Set environment variables
export AZURE_SUBSCRIPTION_ID=${AZURE_SUBSCRIPTION_ID:-"<your_subscription_id>"}
export ACR_NAME=${ACR_NAME:-"<your_acr_name>"}
export RESOURCE_GROUP=${RESOURCE_GROUP:-"<your_resource_group>"}
export TEMPORAL_API_KEY=${TEMPORAL_API_KEY:-"<your_temporal_api_key>"}

echo "Building Docker image for linux/amd64..."
docker buildx build --platform linux/amd64 -t your-app .

echo "Creating ACR instance..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

echo "Logging into ACR..."
az acr login --name $ACR_NAME

echo "Tagging and pushing image to ACR..."
docker tag your-app $ACR_NAME.azurecr.io/your-app:latest
docker push $ACR_NAME.azurecr.io/your-app:latest

echo "Creating Kubernetes namespace..."
kubectl create namespace your-namespace

echo "Applying ConfigMap..."
kubectl apply -f config-map.yaml --namespace your-namespace

echo "Creating Kubernetes secret for Temporal API key..."
kubectl create secret generic temporal-secret \
    --from-literal=TEMPORAL_API_KEY=$TEMPORAL_API_KEY \
    --namespace your-namespace

echo "Deploying to AKS..."
kubectl apply -f deployment.yaml --namespace your-namespace

echo "Deployment complete! Checking pod status..."
kubectl get pods -n your-namespace