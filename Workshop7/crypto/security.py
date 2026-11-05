"""Hybrid secure channel: RSA-OAEP key wrapping + AES-256-GCM + RSA-PSS signature.

Envelope fields (all base64-encoded): encrypted_key, nonce, ciphertext, signature.
"""
import base64
import json
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

OAEP = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)


def _pss():
    return padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)


class SecureChannel:
    def __init__(self, private_key_path: str, peer_public_key_path: str):
        with open(private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(peer_public_key_path, "rb") as f:
            self.peer_public_key = serialization.load_pem_public_key(f.read())

    def encrypt_and_sign(self, payload_dict: dict) -> dict:
        """Signs the JSON with our private key, encrypts it with a fresh AES-256-GCM key,
        and wraps that AES key with the peer's RSA public key."""
        json_bytes = json.dumps(payload_dict).encode("utf-8")

        # 1. Sign the plaintext JSON with our RSA private key
        signature = self.private_key.sign(json_bytes, _pss(), hashes.SHA256())

        # 2. Encrypt the JSON with a fresh symmetric key
        aes_key = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)
        ciphertext = AESGCM(aes_key).encrypt(nonce, json_bytes, None)

        # 3. Wrap the AES key for the peer
        encrypted_aes_key = self.peer_public_key.encrypt(aes_key, OAEP)

        return {
            "encrypted_key": base64.b64encode(encrypted_aes_key).decode("utf-8"),
            "nonce": base64.b64encode(nonce).decode("utf-8"),
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
            "signature": base64.b64encode(signature).decode("utf-8"),
        }

    def decrypt_and_verify(self, envelope: dict) -> dict:
        """Unwraps the AES key, decrypts the JSON, and verifies the peer's signature.
        Raises an exception if the ciphertext or the signature has been tampered with."""
        encrypted_aes_key = base64.b64decode(envelope["encrypted_key"])
        nonce = base64.b64decode(envelope["nonce"])
        ciphertext = base64.b64decode(envelope["ciphertext"])
        signature = base64.b64decode(envelope["signature"])

        aes_key = self.private_key.decrypt(encrypted_aes_key, OAEP)
        json_bytes = AESGCM(aes_key).decrypt(nonce, ciphertext, None)

        self.peer_public_key.verify(signature, json_bytes, _pss(), hashes.SHA256())
        return json.loads(json_bytes.decode("utf-8"))
