import os
import base64
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from config import KEYVAULT_URL, KEYVAULT_SECRET_NAME
_key_cache = None
def get_encryption_key() -> bytes:
    global _key_cache
    if _key_cache:
        return _key_cache
    if not KEYVAULT_URL or not KEYVAULT_SECRET_NAME:
        raise RuntimeError("Azure Key Vault URL and secret name must be set in config.")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KEYVAULT_URL, credential=credential)
    secret = client.get_secret(KEYVAULT_SECRET_NAME)
    try:
        decoded_key = base64.b64decode(secret.value)
        _key_cache = decoded_key
        return decoded_key
    except Exception as e:
        raise ValueError(f"Failed to decode base64 key from Key Vault: {e}") 