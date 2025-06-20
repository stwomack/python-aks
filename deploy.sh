#!/bin/bash

# Source the centralized configuration
source ./source_config.sh

echo "Building Docker image for linux/amd64..."
docker buildx build --platform linux/amd64 -t $APP_NAME .

echo "Creating ACR instance..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

echo "Logging into ACR..."
az acr login --name $ACR_NAME

echo "Tagging and pushing image to ACR..."
docker tag $APP_NAME $ACR_NAME.azurecr.io/$APP_NAME:latest
docker push $ACR_NAME.azurecr.io/$APP_NAME:latest

echo "Creating Kubernetes namespace..."
kubectl create namespace $KUBERNETES_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

echo "Generating Kubernetes manifests from config..."
./generate-k8s-manifests.sh

echo "Applying Secret..."
apply -f acr-secret.yaml --namespace $KUBERNETES_NAMESPACE

echo "Applying ConfigMap..."
kubectl apply -f config-map.yaml --namespace $KUBERNETES_NAMESPACE

echo "Deploying to AKS..."
kubectl apply -f deployment.yaml --namespace $KUBERNETES_NAMESPACE

echo "Deployment complete! Checking pod status..."
kubectl get pods -n $KUBERNETES_NAMESPACE