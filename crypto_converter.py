from temporalio.converter import PayloadConverter, DataConverter, DefaultPayloadConverter
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import json
from keyvault import get_encryption_key

class EncryptedPayloadConverter(PayloadConverter):
    def __init__(self):
        self._key = get_encryption_key()
        if len(self._key) not in (16, 24, 32):
            raise ValueError(f"Encryption key must be 128, 192, or 256 bits. Got {len(self._key)} bytes ({len(self._key) * 8} bits)")
        self._aesgcm = AESGCM(self._key)
        self._default_converter = DefaultPayloadConverter()
    
    @property
    def encoding(self) -> str:
        return "encrypted/aesgcm"
    
    def to_payload(self, value):
        payload = self._default_converter.to_payload(value)
        nonce = os.urandom(12)
        ciphertext = self._aesgcm.encrypt(nonce, payload.data, None)
        encrypted = nonce + ciphertext
        return type(payload)(metadata={"encoding": b"encrypted/aesgcm"}, data=encrypted)
    
    def from_payload(self, payload):
        if payload.metadata.get("encoding") == b"encrypted/aesgcm":
            encrypted = payload.data
            nonce = encrypted[:12]
            ciphertext = encrypted[12:]
            decrypted = self._aesgcm.decrypt(nonce, ciphertext, None)
            decrypted_payload = type(payload)(metadata={"encoding": b"json/plain"}, data=decrypted)
            return self._default_converter.from_payload(decrypted_payload)
        else:
            return self._default_converter.from_payload(payload)
    
    def to_payloads(self, values, *args, **kwargs):
        return [self.to_payload(value) for value in values]
    
    def from_payloads(self, payloads, *args, **kwargs):
        return [self.from_payload(payload) for payload in payloads]

encrypted_converter = DataConverter(payload_converter_class=EncryptedPayloadConverter) 