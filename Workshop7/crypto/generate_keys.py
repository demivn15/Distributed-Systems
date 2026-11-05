"""RSA-2048 key pair generator for the Master and the Node.

Run from the project root:  python -m crypto.generate_keys
"""
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEYS_DIR = "crypto/keys"


def generate_key_pairs(prefix: str):
    os.makedirs(KEYS_DIR, exist_ok=True)
    priv_path = f"{KEYS_DIR}/{prefix}_private.pem"
    pub_path = f"{KEYS_DIR}/{prefix}_public.pem"

    # Never silently overwrite an existing key: the peer would stop trusting us.
    if os.path.exists(priv_path):
        print(f"[Crypto] Keys for '{prefix}' already exist, skipping (delete them to regenerate).")
        return

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    with open(priv_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    with open(pub_path, "wb") as f:
        f.write(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))
    print(f"[Crypto] RSA Keypair generated for '{prefix}'.")


if __name__ == "__main__":
    generate_key_pairs("master")
    generate_key_pairs("node")
