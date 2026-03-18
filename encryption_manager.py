import os
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class EncryptionManager:
    APP_SECRET = b"my_password_manager_secret_2026"
    SALT = b"pm_app_salt_v1"

    def __init__(self):
        kdf = PBKDF2HMAC (
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.SALT,
            iterations=100_000,
            backend=default_backend(),
        )
        self.key = kdf.derive(self.APP_SECRET)

    def encrypt(self, plaintext: str) -> str:
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext.encode("utf-8")) + padder.finalize()

        iv = os.urandom(16)

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend(),
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()

        return base64.b64encode(iv + ciphertext).decode("utf-8")
    
    def decrypt(self, encrypted_b64: str) -> str:
        raw = base64.b64decode(encrypted_b64.encode("utf-8"))
        iv = raw[:16]
        ciphertext = raw[16:]

        cipher = Cipher (
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext_bytes = unpadder.update(padded_plain) + unpadder.finalize()

        return plaintext_bytes.decode("utf-8")
    
    def verify(self, plaintext: str, encrypted_b64: str ) -> bool:
        try:
            return self.decrypt(encrypted_b64) == plaintext
        except Exception:
            return False