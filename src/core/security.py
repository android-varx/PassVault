import string
from datetime import datetime
from typing import List, Tuple, Dict, Any

def check_password_strength(password: str) -> Dict[str, Any]:
    """
    Evaluates the strength of a password.
    Returns a dict with:
      - 'score': int (0 to 5)
      - 'feedback': list of str (suggestions for improvement)
      - 'label': str ('Weak', 'Medium', 'Strong', 'Excellent')
    """
    feedback = []
    score = 0

    # 1. Length Check
    length = len(password)
    if length < 8:
        feedback.append("Password must be at least 8 characters long.")
    elif length >= 16:
        score += 2
    elif length >= 12:
        score += 1

    # 2. Character diversity checks
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    if not has_upper:
        feedback.append("Add uppercase letters (A-Z).")
    else:
        score += 1

    if not has_lower:
        feedback.append("Add lowercase letters (a-z).")
        
    if not has_digit:
        feedback.append("Add numbers (0-9).")
    else:
        score += 1

    if not has_symbol:
        feedback.append("Add special characters/symbols (e.g. @, #, $, !).")
    else:
        score += 1

    # 3. Check for extremely common patterns
    common_patterns = ["123456", "password", "qwerty", "admin", "passvault", "12345678"]
    pwd_lower = password.lower()
    for pattern in common_patterns:
        if pattern in pwd_lower:
            score = max(0, score - 1)
            feedback.append(f"Avoid common sequences or terms like '{pattern}'.")
            break

    # Cap score
    score = min(5, max(0, score)) if length >= 8 else 1
    if length == 0:
        score = 0

    labels = {
        0: ("Very Weak", "#FF3333"),
        1: ("Weak", "#FF5722"),
        2: ("Fair", "#FFC107"),
        3: ("Medium", "#FFEB3B"),
        4: ("Strong", "#4CAF50"),
        5: ("Excellent", "#00E676")
    }
    
    label, color = labels.get(score, ("Weak", "#FF5722"))

    return {
        "score": score,
        "feedback": feedback,
        "label": label,
        "color": color
    }

class VaultAuditor:
    def __init__(self, db_manager, crypto_manager):
        self.db = db_manager
        self.crypto = crypto_manager

    def run_audit(self) -> Dict[str, Any]:
        """
        Scans all vault credentials and flags weaknesses:
        - Weak passwords (strength score < 4)
        - Reused passwords
        - Old passwords (not updated in > 180 days)
        Returns audit statistics and issue lists.
        """
        all_creds = self.db.get_all_credentials()
        total_accounts = len(all_creds)

        weak_accounts = []
        password_occurrences = {} # decrypted_pwd -> list of (id, site, username)
        old_accounts = []

        now = datetime.now()

        for cred_id, site, username, encrypted_pwd, category, created_at, updated_at in all_creds:
            try:
                decrypted = self.crypto.decrypt(encrypted_pwd)
            except Exception:
                # Skip undecryptable passwords
                continue

            # 1. Check Strength
            strength = check_password_strength(decrypted)
            if strength["score"] < 4:
                weak_accounts.append({
                    "id": cred_id,
                    "site": site,
                    "username": username,
                    "score": strength["score"],
                    "label": strength["label"],
                    "reasons": strength["feedback"]
                })

            # 2. Track for Reused Passwords
            if decrypted not in password_occurrences:
                password_occurrences[decrypted] = []
            password_occurrences[decrypted].append({
                "id": cred_id,
                "site": site,
                "username": username
            })

            # 3. Check Age (Old passwords > 180 days)
            try:
                updated_date = datetime.fromisoformat(updated_at)
                age_days = (now - updated_date).days
                if age_days > 180:
                    old_accounts.append({
                        "id": cred_id,
                        "site": site,
                        "username": username,
                        "days_old": age_days
                    })
            except Exception:
                pass

        # Parse duplicate/reused accounts
        reused_details = []
        for pwd, accs in password_occurrences.items():
            if len(accs) > 1:
                reused_details.append({
                    "password_preview": pwd[:3] + "*" * min(5, len(pwd) - 3) if len(pwd) > 3 else "***",
                    "accounts": accs
                })

        # Calculate security score
        # Start at 100, deduct points for security flaws:
        # -15 per weak password (cap at 40)
        # -15 per duplicate group (cap at 40)
        # -5 per old password (cap at 20)
        score = 100
        
        if total_accounts > 0:
            weak_deductions = len(weak_accounts) * 15
            reused_deductions = len(reused_details) * 15
            old_deductions = len(old_accounts) * 5

            score -= min(40, weak_deductions)
            score -= min(40, reused_deductions)
            score -= min(20, old_deductions)

        score = max(0, min(100, score))

        return {
            "security_score": score,
            "total_accounts": total_accounts,
            "weak_accounts": weak_accounts,
            "reused_accounts": reused_details,
            "old_accounts": old_accounts
        }
