kubectl patch configmap temporal-worker-config --patch '{"data":{"TEMPORAL_ADDRESS":"host.docker.internal:7233"}}'
