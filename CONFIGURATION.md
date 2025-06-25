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
- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_SECRET`
- `KEYVAULT_URL`
- `KEYVAULT_SECRET_NAME`

## Example config.env

```bash
# Azure Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
ACR_NAME=womackecr
RESOURCE_GROUP=aks-temporal
AZURE_CLIENT_ID=your-service-principal-client-id
AZURE_TENANT_ID=your-azure-tenant-id
AZURE_CLIENT_SECRET=your-service-principal-client-secret

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

# Azure Key Vault for Encryption (required for encryption)
KEYVAULT_URL=https://your-keyvault-name.vault.azure.net/
KEYVAULT_SECRET_NAME=temporal-encryption-key
```

## Azure Service Principal Setup

This project uses Azure service principal authentication to access Azure Key Vault. You need to create a service principal and grant it appropriate permissions.

### Creating a Service Principal

```bash
az ad sp create-for-rbac --name <your-app-name> --role Contributor --scopes /subscriptions/<subscription-id>
```

This command outputs a JSON object containing:
- `appId` → Use as `AZURE_CLIENT_ID`
- `tenant` → Use as `AZURE_TENANT_ID`  
- `password` → Use as `AZURE_CLIENT_SECRET`

### Granting Key Vault Access

For RBAC-enabled Key Vaults (recommended):
```bash
az role assignment create \
  --assignee <service-principal-client-id> \
  --role "Key Vault Secrets User" \
  --scope "/subscriptions/<subscription-id>/resourcegroups/<resource-group>/providers/microsoft.keyvault/vaults/<keyvault-name>"
```

For Access Policy Key Vaults (legacy):
```bash
az keyvault set-policy --name <keyvault-name> --spn <service-principal-client-id> --secret-permissions get list
```

## Azure Key Vault Integration for Payload Encryption

This project supports encrypting all Temporal workflow/activity payloads using a symmetric key stored in Azure Key Vault. The key is fetched at runtime using Azure service principal authentication and used for AES-GCM encryption/decryption via a custom PayloadConverter.

### Required Configuration
Add the following to your `config.env` (these must be set for encryption to work):

```
KEYVAULT_URL=https://your-keyvault-name.vault.azure.net/
KEYVAULT_SECRET_NAME=temporal-encryption-key
```

- `KEYVAULT_URL`: The full URL of your Azure Key Vault instance. **Required for encryption.**
- `KEYVAULT_SECRET_NAME`: The name of the secret in Key Vault containing your base64-encoded AES key (128, 192, or 256 bits). **Required for encryption.**

These must be set as environment variables or in your `config.env` file. There are no defaults or fallbacks for these values.

### Setting up the Key in Azure Key Vault
1. Generate a random 256-bit key (recommended):
   ```bash
   openssl rand -base64 32
   ```

2. **Set up permissions for your service principal:**

   **Important:** Your Key Vault may use RBAC authorization (modern) or Access Policies (legacy). Check your Key Vault's "Access control (IAM)" page in Azure Portal.

   **For RBAC-enabled Key Vaults (recommended):**
   ```bash
   # Assign Key Vault Secrets User role to your service principal
   az role assignment create \
     --assignee <service-principal-client-id> \
     --role "Key Vault Secrets User" \
     --scope "/subscriptions/<subscription-id>/resourcegroups/<resource-group>/providers/microsoft.keyvault/vaults/<keyvault-name>"
   ```

   **For Access Policy Key Vaults (legacy):**
   ```bash
   az keyvault set-policy --name <keyvault-name> --spn <service-principal-client-id> --secret-permissions get list
   ```

3. Store it as a secret in your Key Vault:
   ```bash
   az keyvault secret set --vault-name <keyvault-name> --name temporal-encryption-key --value <your-base64-key>
   ```

### How it Works
- On startup, the worker and client authenticate to Azure using the service principal credentials.
- The encryption key is fetched from Key Vault using the authenticated service principal.
- All workflow/activity payloads are transparently encrypted before being sent to Temporal, and decrypted on receipt.
- The key is never stored in code or config files.

### Additional Dependencies
Add these to your requirements:
- `azure-identity`
- `azure-keyvault-secrets`
- `cryptography`

Install with:
```bash
pip install azure-identity azure-keyvault-secrets cryptography
``` 