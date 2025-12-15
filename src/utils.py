import string
import random
import os

def generate_password(length: int = 12, use_upper: bool = True, use_digits: bool = True, use_symbols: bool = True) -> str:
    """Generates a secure random password."""
    chars = string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    return ''.join(random.choice(chars) for _ in range(length))

def is_password_secure(password: str) -> bool:
    """
    Checks if a password meets security requirements:
    - At least 8 characters
    - Contains uppercase
    - Contains lowercase
    - Contains digit
    - Contains symbol
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in string.punctuation for c in password):
        return False
    return True

def get_asset_path(filename: str) -> str:
    """Returns the absolute path to an asset."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # src/.. -> root
    return os.path.join(base_dir, "assets", filename)
