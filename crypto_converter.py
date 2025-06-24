from temporalio.converter import PayloadConverter, DataConverter, DefaultPayloadConverter
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import json
from keyvault import get_encryption_key

class EncryptedPayloadConverter(PayloadConverter):
    """
    Encrypts and decrypts payloads using AES-GCM with a key from Azure Key Vault.
    """
    def __init__(self):
        self._key = get_encryption_key()
        if isinstance(self._key, str):
            self._key = self._key.encode()
        if len(self._key) not in (16, 24, 32):
            raise ValueError("Encryption key must be 128, 192, or 256 bits.")
        self._aesgcm = AESGCM(self._key)
        self._underlying = DefaultPayloadConverter()

    @property
    def encoding(self) -> str:
        return "encrypted/aesgcm"

    def to_payload(self, value):
        # Serialize using the default converter
        payload = self._underlying.to_payload(value)
        # Encrypt the payload data
        nonce = os.urandom(12)
        ciphertext = self._aesgcm.encrypt(nonce, payload.data, None)
        # Store nonce + ciphertext
        encrypted = nonce + ciphertext
        return type(payload)(
            metadata={"encoding": b"encrypted/aesgcm"},
            data=encrypted
        )

    def from_payload(self, payload):
        # Decrypt the payload data
        encrypted = payload.data
        nonce = encrypted[:12]
        ciphertext = encrypted[12:]
        decrypted = self._aesgcm.decrypt(nonce, ciphertext, None)
        # Use the default converter to deserialize
        return self._underlying.from_payload(type(payload)(metadata=payload.metadata, data=decrypted))

    def to_payloads(self, values):
        return [self.to_payload(value) for value in values]

    def from_payloads(self, payloads):
        return [self.from_payload(payload) for payload in payloads]

# For use in DataConverter
encrypted_converter = DataConverter([EncryptedPayloadConverter()]) 