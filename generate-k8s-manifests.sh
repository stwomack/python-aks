#!/bin/bash

# Source the centralized configuration
source ./source_config.sh

echo "Generating Kubernetes manifests from config..."

# Generate ACR Secret
DOCKER_AUTH=$(echo -n "$ACR_USERNAME:$ACR_PASSWORD" | base64)
DOCKER_CONFIG=$(echo -n "{\"auths\":{\"$ACR_NAME.azurecr.io\":{\"username\":\"$ACR_USERNAME\",\"password\":\"$ACR_PASSWORD\",\"email\":\"$ACR_EMAIL\",\"auth\":\"$DOCKER_AUTH\"}}}" | base64 -w0)

cat > acr-secret.yaml << EOF
apiVersion: v1
kind: Secret
metadata:
  name: acr-secret
  namespace: $KUBERNETES_NAMESPACE
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: $DOCKER_CONFIG
EOF

echo "  - acr-secret.yaml"

# Generate ConfigMap
cat > config-map.yaml << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: temporal-worker-config
  namespace: $KUBERNETES_NAMESPACE
data:
  TEMPORAL_ADDRESS: "$TEMPORAL_ADDRESS"
  TEMPORAL_NAMESPACE: "$TEMPORAL_NAMESPACE"
  TEMPORAL_TASK_QUEUE: "$TEMPORAL_TASK_QUEUE"
EOF

echo "  - config-map.yaml"

# Generate Deployment
cat > deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
   name: $APP_NAME
   namespace: $KUBERNETES_NAMESPACE
   labels:
      app: $APP_NAME
spec:
   selector:
      matchLabels:
         app: $APP_NAME
   replicas: 1
   template:
      metadata:
         labels:
            app: $APP_NAME
      spec:
         imagePullSecrets:
         - name: acr-secret
         containers:
            - name: $APP_NAME
              image: $APP_IMAGE
              env:
                - name: TEMPORAL_ADDRESS
                  valueFrom:
                    configMapKeyRef:
                      name: temporal-worker-config
                      key: TEMPORAL_ADDRESS
                - name: TEMPORAL_NAMESPACE
                  valueFrom:
                    configMapKeyRef:
                      name: temporal-worker-config
                      key: TEMPORAL_NAMESPACE
                - name: TEMPORAL_TASK_QUEUE
                  valueFrom:
                    configMapKeyRef:
                      name: temporal-worker-config
                      key: TEMPORAL_TASK_QUEUE
                - name: TEMPORAL_API_KEY
                  valueFrom:
                    secretKeyRef:
                      name: temporal-secret
                      key: TEMPORAL_API_KEY
              resources:
                limits:
                  cpu: "$CPU_LIMIT"
                  memory: "$MEMORY_LIMIT"
                requests:
                  cpu: "$CPU_REQUEST"
                  memory: "$MEMORY_REQUEST"
EOF

echo "  - deployment.yaml"

echo "Kubernetes manifests generated successfully!"
