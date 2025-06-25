from temporalio.converter import PayloadConverter, DataConverter, DefaultPayloadConverter
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import json
from keyvault import get_encryption_key

class EncryptedPayloadConverter(PayloadConverter):
    def __init__(self):
        self._key = get_encryption_key()
        print(f"DEBUG: Key length is {len(self._key)} bytes")
        print(f"DEBUG: Key (first 10 bytes): {self._key[:10] if len(self._key) >= 10 else self._key}")
        if len(self._key) not in (16, 24, 32):
            raise ValueError(f"Encryption key must be 128, 192, or 256 bits. Got {len(self._key)} bytes ({len(self._key) * 8} bits)")
        self._aesgcm = AESGCM(self._key)
        self._underlying = DefaultPayloadConverter()
    @property
    def encoding(self) -> str:
        return "encrypted/aesgcm"
    def to_payload(self, value):
        payload = self._underlying.to_payload(value)
        nonce = os.urandom(12)
        ciphertext = self._aesgcm.encrypt(nonce, payload.data, None)
        encrypted = nonce + ciphertext
        return type(payload)(metadata={"encoding": b"encrypted/aesgcm"}, data=encrypted)
    def from_payload(self, payload):
        encrypted = payload.data
        nonce = encrypted[:12]
        ciphertext = encrypted[12:]
        decrypted = self._aesgcm.decrypt(nonce, ciphertext, None)
        return self._underlying.from_payload(type(payload)(metadata=payload.metadata, data=decrypted))
    def to_payloads(self, values):
        return [self.to_payload(value) for value in values]
    def from_payloads(self, payloads):
        return [self.from_payload(payload) for payload in payloads]

class EncryptedDataConverter(DataConverter):
    def __init__(self):
        super().__init__()
        self._encrypted_converter = EncryptedPayloadConverter()
        self._default_converter = DefaultPayloadConverter()
    def to_payload(self, value):
        return self._encrypted_converter.to_payload(value)
    def from_payload(self, payload):
        if payload.metadata.get("encoding") == b"encrypted/aesgcm":
            return self._encrypted_converter.from_payload(payload)
        else:
            return self._default_converter.from_payload(payload)
encrypted_converter = EncryptedDataConverter() 