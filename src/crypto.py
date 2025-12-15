import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoManager:
    def __init__(self, master_password: str):
        """
        Initializes the CryptoManager with a master password.
        The salt is stored in a file 'salt.key'. If it doesn't exist, it's created.
        """
        self.salt_file = "salt.key"
        self.salt = self._load_or_create_salt()
        self.key = self._derive_key(master_password, self.salt)
        self.fernet = Fernet(self.key)

    def _load_or_create_salt(self) -> bytes:
        if os.path.exists(self.salt_file):
            with open(self.salt_file, "rb") as f:
                return f.read()
        else:
            salt = os.urandom(16)
            with open(self.salt_file, "wb") as f:
                f.write(salt)
            return salt

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derives a url-safe base64-encoded key from the password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt(self, plaintext: str) -> str:
        """Encrypts a plaintext string."""
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypts a ciphertext string."""
        try:
            return self.fernet.decrypt(ciphertext.encode()).decode()
        except Exception:
            raise ValueError("Decryption failed. Wrong master password?")

    @staticmethod
    def verify_master_password_check(master_password: str) -> bool:
        """
        To verify if the master password is correct without decrypting everything,
        we usually try to decrypt a known token. 
        For this simple app, we can just rely on the fact that if decryption fails, 
        the password is wrong. 
        
        However, to improve UX on login, we'll implement a simple 'check file'.
        """
        pass # Logic handled in UI (try decrypting a dummy value or the DB)
