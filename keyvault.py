import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from config import KEYVAULT_URL, KEYVAULT_SECRET_NAME

_key_cache = None

def get_encryption_key() -> str:
    global _key_cache
    if _key_cache:
        return _key_cache
    if not KEYVAULT_URL or not KEYVAULT_SECRET_NAME:
        raise RuntimeError("Azure Key Vault URL and secret name must be set in config.")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KEYVAULT_URL, credential=credential)
    secret = client.get_secret(KEYVAULT_SECRET_NAME)
    _key_cache = secret.value
    return _key_cache 