```   az ad sp create-for-rbac --name <your-app-name> --role Contributor --scopes /subscriptions/<subscription-id>```

```az role assignment create --assignee spid --role "Key Vault Secrets User" --scope "/subscriptions/id/resourcegroups/aks-temporal/providers/microsoft.keyvault/vaults/my-key-vault"```