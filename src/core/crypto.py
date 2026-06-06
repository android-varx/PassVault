import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoManager:
    def __init__(self, master_password: str, db_manager):
        """
        Initializes the CryptoManager with a master password and database manager.
        The salt is loaded from/stored in the SQLite database configuration table.
        It also handles migrating legacy 'salt.key' file to the database.
        """
        self.db = db_manager
        self.salt = self._load_or_create_salt()
        self.key = self._derive_key(master_password, self.salt)
        self.fernet = Fernet(self.key)

    def _load_or_create_salt(self) -> bytes:
        # 1. Try to get salt from database
        salt = self.db.get_salt()
        if salt:
            return salt

        # 2. Migration fallback: check if legacy 'salt.key' exists in execution directory
        legacy_salt_file = "salt.key"
        if os.path.exists(legacy_salt_file):
            try:
                with open(legacy_salt_file, "rb") as f:
                    salt = f.read()
                # Migrate to database
                self.db.set_salt(salt)
                # Safely delete legacy file
                os.remove(legacy_salt_file)
                return salt
            except Exception as e:
                print(f"Error migrating legacy salt file: {e}")

        # 3. Create fresh salt if none existed
        salt = os.urandom(16)
        self.db.set_salt(salt)
        return salt

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derives a url-safe base64-encoded key from the password."""
        # V3.0 uses 600,000 PBKDF2 iterations for stronger resistance to brute force
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000,
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
